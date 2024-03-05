import threading

# Define a thread-local storage dictionary to hold the request object
thread_local = threading.local()


# Middleware to store the request object in the local thread
class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the request object in the local thread
        thread_local.request = request
        response = self.get_response(request)
        return response


def get_request():
    return getattr(thread_local, 'request', None)
