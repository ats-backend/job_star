import logging
import os
from decouple import config

from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

log = logging.getLogger(__name__)


class ResponseLoggingMiddleware(MiddlewareMixin):
    req = None
    request_by= None
    admin_frontend = None

    def basicConfig(self, **messages):

        website_api_key = self.req.META.get('HTTP_API_KEY')
        if website_api_key == config('API_KEY'):
            self.request_by = 'website frontend'
        else:
            self.request_by = 'admin frontend'

        with open(file='app_jobs.log', mode='a') as file:
            handler = file.write(
                f'Time: {messages["time"]}' + "  "
                f'Method:{self.req.method}' + "  "
                f'Request_by:{self.request_by}' + "  "
                f'Status_code:{messages["method"]}' + " "
                f"Endpoint: {messages['endpoint']}\n"
            )

            return handler

    def process_response(self, request, response):
        self.req = request
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
