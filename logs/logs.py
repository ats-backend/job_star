import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


log = logging.getLogger(__name__)


class ResponseLoggingMiddleware(MiddlewareMixin):
    req = None
    action = None

    def basicConfig(self, **messages):

        with open(file='app_jobs.log', mode='a') as file:
            handler = file.write(
                f'Time: {messages["time"]}' + "  "
                f'Method:{self.req.method}' + "  "
                f"Action:{self.req.body}" + "  "
                f'Status_code:{messages["method"]}' + " "
                f"Endpoint: {messages['endpoint']}\n"
            )

            return handler

    def process_response(self, request, response):
        try:

            log.info(self.basicConfig(
                time=timezone.now(),
                filename="app_jobs.log",
                method=f'{response.status_code}',
                endpoint=f"{request.META['REMOTE_ADDR']}"
                         f"{request.get_full_path()}"
            ))
        except Exception as e:
            log.error(f'RequestLoggingMiddleware error : {e}')

        return response
