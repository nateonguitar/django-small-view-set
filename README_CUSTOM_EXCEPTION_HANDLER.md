# Handling Endpoint Exceptions

This guide explains how to make a custom exception handler that will map `Exceptions` to `JsonResponses`.

## Using the @endpoint Decorator

The library provides an `@endpoint` decorator to allow http methods and to route thrown exceptions to your custom exception handler.

Register SmallViewSetConfig in settings.py
```python
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(
    exception_handler=app_exception_handler)
```

## Creating a Custom Exception Handler

Assume you have some custom exception defined:

```python
class CustomException(Exception):
    def __init__(self, message, data):
        self.message = message
        self.data = data
```

Define a custom exception handler to catch specific exceptions and return custom responses.

```python
from django.http import JsonResponse
from urllib.request import Request
from small_view_set import default_exception_handler


def app_exception_handler(request: Request, endpoint_name: str, exception):
    if isinstance(exception, CustomException):
        return JsonResponse(
            data={ "error": exception.message, "data": exception.data },
            status=400)

    # For convenience, you may want to fallback to the default exception handler
    # which will detect most exceptions that look like response errors
    # like PermissionDenied or Http404. All others will result in a 500 response.

    # When settings DEBUG=True more details will be logged when any 5XX response is caught.

    # default_exception_handler is available for copying if needed for inspiration in
    # your own code base.
    return default_exception_handler(request, endpoint_name, exception)
```

Or if you like the try/except pattern better:

```python
def app_exception_handler(request: Request, endpoint_name: str, exception):
    try:
        raise exception
    except CustomException:
        return JsonResponse(
            data={ "error": exception.message, "data": exception.data },
            status=400)
    except Exception:
        return default_exception_handler(request, endpoint_name, exception)
```

With this setup, any `CustomException` raised in your endpoints will be caught by `app_exception_handler`, and a custom JSON response will be returned.

## OPTIONS and HEAD request handling

`SmallViewSetConfig` also has an `options_and_head_handler` parameter if you need to customize how
your application will handle those requests. It looks a lot like an endpoint in a viewset,
feel free to copy the `default_options_and_head_handler` and customize it.

It gets the `allowed_methods` from the `@endpoint(allowed_methods=['POST'])` decorator on endpoints.

```
def default_options_and_head_handler(request: Request, allowed_methods: list[str]):
    if request.method == 'OPTIONS':
            response = JsonResponse(
                data=None,
                safe=False,
                status=200,
                content_type='application/json')
            response['Allow'] = ', '.join(allowed_methods)
            return response

    if request.method == 'HEAD':
        response = JsonResponse(
            data=None,
            safe=False,
            status=200,
            content_type='application/json')
        response['Allow'] = ', '.join(allowed_methods)
        return response

    if request.method not in allowed_methods:
        raise MethodNotAllowed(method=request.method)
```

Register SmallViewSetConfig in settings.py

```python
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(
    exception_handler=app_exception_handler,
    options_and_head_handler=app_options_and_head_handler)
```