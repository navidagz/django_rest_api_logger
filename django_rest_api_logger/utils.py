from django.utils.timezone import now


def get_ip_address(request):
    ip_addr = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip_addr:
        return ip_addr.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def get_token(request):
    try:
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        auth_header = auth.encode('iso-8859-1')
        if not auth_header:
            return None
        return auth_header[1].decode('utf-8')
    except:
        return None


def get_user(request):
    return request.user.__str__()


def get_response_ms(start):
    response_timedelta = now() - start
    response_ms = int(response_timedelta.total_seconds() * 1000)
    return max(response_ms, 0)
