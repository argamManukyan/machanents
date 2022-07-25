from django.utils.deprecation import MiddlewareMixin


class CoreMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        print(exception)