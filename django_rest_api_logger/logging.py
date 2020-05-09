import ast
import json
import traceback

from django.core.files.uploadedfile import UploadedFile
from django.db import connection
from django.utils.timezone import now
from rest_framework.views import APIView

from .logger import logger
from .mongo_config import MONGO_HOST, MONGO_LOG_COLLECTION, log_db
from .utils import get_token, get_user, get_ip_address, get_response_ms


class APILoggingMixin:
    CLEANED_SUBSTITUTE = '****'
    LOGGING_METHODS = '__all__'
    SENSITIVE_FIELDS = {'api', 'token', 'key', 'secret', 'password', 'signature', "confirm_password"}

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a string.'
        assert APIView in self.__class__.mro(), "Super class should be inherited from APIView"

        self.requested_at = None
        self.log = dict()

        super(APILoggingMixin, self).__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self.requested_at = now()
        self.log['requested_at'] = str(self.requested_at)
        self.log['data'] = self._clean_data(request.body)

        super(APILoggingMixin, self).initial(request, *args, **kwargs)

        try:
            data = self.request.data.dict()
        except AttributeError:
            data = self.request.data

        self.log['data'] = self._clean_data(data)

    def handle_exception(self, exc):
        try:
            response = super(APILoggingMixin, self).handle_exception(exc)
            return response
        except Exception as e:
            self.log['errors'] = {num: line for num, line in enumerate(traceback.format_exc().split("\n"))}

    def finalize_response(self, request, response, *args, **kwargs):
        try:
            response = super(APILoggingMixin, self).finalize_response(request, response, *args, **kwargs)
        except:
            response = None

        should_log = self._should_log if hasattr(self, '_should_log') else self.should_log

        if should_log(request, response):
            try:
                app = str(self._get_view_name(request)).split('.')[2]
            except:
                app = ""

            self.log.update(
                {
                    'remote_addr': get_ip_address(request),
                    'view': self._get_view_name(request),
                    'app': app,
                    'view_method': self._get_view_method(request),
                    'path': request.path,
                    'host': request.get_host(),
                    'method': request.method,
                    'query_params': self._clean_data(request.query_params.dict()),
                    'user': get_user(request),
                    'response_ms': get_response_ms(self.requested_at),
                    'token': get_token(request)
                }
            )

            if response:
                if hasattr(response, 'rendered_content'):
                    rendered_content = response.rendered_content
                else:
                    rendered_content = response.getvalue()

                self.log.update(
                    {
                        'status_code': response.status_code,
                        'response': self._clean_data(json.loads(rendered_content.decode()))
                    }
                )
                try:
                    if not connection.settings_dict.get('ATOMIC_REQUESTS'):
                        self.handle_log()
                    elif response.exception and not connection.in_atomic_block or not response.exception:
                        self.handle_log()
                    elif response.exception:
                        connection.set_rollback(True)
                        connection.set_rollback(False)
                        self.handle_log()
                except Exception:
                    logger.info('Logging API call raise exception!')
            else:
                self.log.update(
                    {
                        'response': None,
                        'status_code': 500
                    }
                )
                try:
                    self.handle_log()
                except Exception:
                    logger.info('Logging API call raise exception!')

        return response

    def handle_log(self):
        try:
            if MONGO_HOST:
                if "_id" in self.log.keys():
                    # Handle duplicate records
                    self.log.pop("_id", None)
                log_db[MONGO_LOG_COLLECTION].insert(self.log)

            if logger.handlers:
                logger.info(self.log)
        except Exception as e:
            logger.info("ERROR: {}".format(e.args))

    def _get_view_name(self, request):
        method = request.method.lower()
        try:
            attributes = getattr(self, method)
            view_name = (type(attributes.__self__).__module__ + '.' +
                         type(attributes.__self__).__name__)
            return view_name
        except AttributeError:
            return None

    def _get_view_method(self, request):
        if hasattr(self, 'action'):
            return self.action if self.action else None
        return request.method.lower()

    def should_log(self, request):
        return self.LOGGING_METHODS == '__all__' or request.method in self.LOGGING_METHODS

    def _clean_data(self, data):
        if isinstance(data, bytes):
            data: bytes = data.decode(errors='replace')
        elif isinstance(data, list):
            return [self._clean_data(d) for d in data]
        elif isinstance(data, dict):
            data: dict = dict(data)

            if self.SENSITIVE_FIELDS:
                self.SENSITIVE_FIELDS = self.SENSITIVE_FIELDS | {field.lower() for field in self.SENSITIVE_FIELDS}

            for key, value in data.items():
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass

                if isinstance(value, list) or isinstance(value, dict):
                    data[key] = self._clean_data(value)
                elif isinstance(value, UploadedFile):
                    data[key] = value.name

                if key.lower() in self.SENSITIVE_FIELDS:
                    data[key] = self.CLEANED_SUBSTITUTE
        return data
