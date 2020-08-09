import datetime
from threading import Thread

import certifi
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError


def __send_to_es(timestamp, message):
    index = getattr(settings, "DRF_LOGGER_ELASTICSEARCH_INDEX", "django_rest_api_logger")
    if getattr(settings, "DRF_LOGGER_ELASTICSEARCH_ENABLED", False):
        elasticsearch_ssl = getattr(settings, "DRF_LOGGER_ELASTICSEARCH_SSL", False)
        elasticsearch_hosts = getattr(settings, "DRF_LOGGER_ELASTICSEARCH_HOSTS", [])
        elasticsearch_auth = getattr(settings, "DRF_LOGGER_ELASTICSEARCH_AUTH", None)

        try:
            conn = Elasticsearch(hosts=elasticsearch_hosts,
                                 use_ssl=elasticsearch_ssl,
                                 http_auth=elasticsearch_auth,
                                 verify_certs=elasticsearch_ssl,
                                 ca_certs=certifi.where())
        except Exception as e:
            import traceback
            traceback.print_exc()
        try:
            conn.index(
                index="{}".format(index),
                body={
                    "date": datetime.datetime.fromtimestamp(timestamp.timestamp()).isoformat(),
                    "message": message
                })
        except ConnectionError:
            pass


def send_to_elasticsearch(timestamp, message):
    Thread(target=__send_to_es, args=(timestamp, message)).start()
