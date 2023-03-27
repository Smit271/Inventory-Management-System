from django.utils.deprecation import MiddlewareMixin
from accounts.models import User


class CreatorModifierMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        if not hasattr(request, 'creator'):
            print("====> request: ", request)
            setattr(request, 'creator', request.user)

        setattr(request, 'modifier', request.user)

    def process_response(self, request, response):
        return response
