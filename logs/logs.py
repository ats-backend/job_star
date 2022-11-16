from datetime import datetime
import logging
from django.utils.deprecation import MiddlewareMixin


log = logging.getLogger(__name__)


class ResponseLoggingMiddleware(MiddlewareMixin):
    req = None

    def basicConfig(self, **messages):

        with open(file='logs.txt', mode='a') as file:
            handler = file.write(
                f'Time: {messages["time"]}' + "  "
                f'Method:{self.req.method}' + "  "
                f'Status_code:{messages["method"]}' + " "
                f"Endpoint: {messages['endpoint']}\n"
            )

            return handler

    def process_response(self, request, response):
        self.req = request
        try:

            log.info(self.basicConfig(
                time=datetime.now(),
                filename="logs.txt",
                method=f'{response.status_code}',
                endpoint=f"{request.META['REMOTE_ADDR']}"
                         f"{request.get_full_path()}"
            ))
        except Exception as e:
            log.error(f'RequestLoggingMiddleware error : {e}')

        return response
