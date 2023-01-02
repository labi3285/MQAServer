import logging
logger = logging.getLogger('django')

from django.utils.deprecation import MiddlewareMixin
from aws_mqaserver.utils import response

# Catch api Exceptions globaly
class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(exception)
        return response.ResponseError('%s'%exception)
        