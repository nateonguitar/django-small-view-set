# Handling Endpoint Exceptions

This guide explains how to handle exceptions in your endpoints and customize the behavior.

## Using the @endpoint Decorator

The library provides an `@endpoint` decorator to handle common API errors gracefully. Here’s an example:

Register SmallViewSetConfig in settings.py
```python
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(
    exception_handler=app_exception_handler)
```

```python
from small_view_set import SmallViewSet, endpoint, SmallViewSetConfig

class MyViewSet(SmallViewSet):

    @endpoint(allowed_methods=['GET'])
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)
```

## Creating a Custom Exception Handler

Define a custom exception handler to catch specific exceptions and return custom responses.

```python
from django.http import JsonResponse
from urllib.request import Request
from small_view_set import default_exception_handler

class CustomException(Exception):
    pass

def app_exception_handler(request: Request, endpoint_name: str, exception):
    if isinstance(exception, CustomException):
        return JsonResponse(
            data={ "error": "A custom exception occurred" },
            status=400)

    # For convenience, you may want to fallback to the default exception handler
    # which will detect most exceptions that look like response errors
    # like PermissionDenied or Http404. All others will result in a 500 response.
    # When settings DEBUG=True more details will be logged when any 5XX response is caught.

    # Feel free to copy from the default exception handler for inspiration in
    # your own code base
    return default_exception_handler(request, endpoint_name, exception)
```

Or if you like the try/except pattern better:

```python
def app_exception_handler(request: Request, endpoint_name: str, exception):
    try:
        raise exception
    except CustomException:
        return JsonResponse(
            data={ "error": "A custom exception occurred" },
            status=400)
    except Exception:
        # Or your own default logic
        return default_exception_handler(request, endpoint_name, exception)
```

With this setup, any `CustomException` raised in your endpoints will be caught by `app_exception_handler`, and a custom JSON response will be returned.
