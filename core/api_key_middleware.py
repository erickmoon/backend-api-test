from django.http import JsonResponse
from django.conf import settings

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to media files without API key
        if request.path.startswith('/media/'):
            return self.get_response(request)

        # Check for the API key in the request headers
        api_key = request.headers.get("X-API-Key")

        # If the API key is not present or doesn't match, return an error response
        if not api_key or api_key != settings.API_KEY:
            return JsonResponse({"error": "Invalid or missing API key"}, status=403)

        # If the API key is valid, allow the request to proceed
        response = self.get_response(request)
        return response