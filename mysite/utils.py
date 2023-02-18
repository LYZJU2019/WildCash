import requests
from .models import *

def get_login_ip(request):
    """
    Get the IP address of the user who is logging in
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_login_country(request):
    """
    Get the country of the user who is logging in
    """
    ip = get_login_ip(request)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()['country']
    except:
        return None