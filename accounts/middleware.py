from django.utils import timezone
import os
from django.conf import settings

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now().strftime("%Y-%m-%d %H:%M")
        username = request.user.username if request.user.is_authenticated else "AnonymousUser"
        ip = request.META.get('REMOTE_ADDR', '')
        path = request.path
        
        log_file = os.path.join(settings.BASE_DIR, 'requests.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{now}]\nUser: {username}\nIP: {ip}\nPath: {path}\n----------------------------------\n")

        response = self.get_response(request)
        return response
