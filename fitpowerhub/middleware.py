from django.utils import timezone
from store.models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
                timestamp=timezone.now()
            )
        
        return response