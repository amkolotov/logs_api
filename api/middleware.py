import logging

from django.http import JsonResponse

logger = logging.getLogger('api')


class ProcessException:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        logger.exception(exception)
        return JsonResponse({'status': 'error', 'description': str(exception)}, status=500)
