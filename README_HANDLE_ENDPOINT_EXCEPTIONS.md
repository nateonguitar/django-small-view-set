# Handling Endpoint Exceptions

This guide explains how to handle exceptions in your endpoints and customize the behavior.

## Using the @endpoint Decorator

The library provides an `@endpoint` decorator to handle common API errors gracefully. Here’s an example:

```python
from small_view_set import SmallViewSet
from small_view_set.decorators import endpoint
from small_view_set.config import SmallViewSetConfig

# Register SmallViewSetConfig in settings
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()

class MyViewSet(SmallViewSet):

    @endpoint(allowed_methods=['GET'])
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)
```

## Writing Your Own Decorator

You can write your own decorator by copying the `@endpoint` implementation and customizing it for your app. For example:

```python
from small_view_set.decorators import endpoint

def custom_endpoint(allowed_methods):
    return endpoint(allowed_methods=allowed_methods)

class MyViewSet(SmallViewSet):

    @custom_endpoint(allowed_methods=['POST'])
    def create(self, request, *args, **kwargs):
        self.protect_create(request)
        return JsonResponse({"message": "Created!"}, status=201)
```

## Creating a Custom Exception Handler

You can define a custom exception handler to catch specific exceptions and return custom responses. Here’s an example:

```python
from django.http import JsonResponse
from urllib.request import Request
from small_view_set.helpers import default_exception_handler

class CustomException(Exception):
    pass

def app_exception_handler(request: Request, endpoint_name: str, exception):
    if isinstance(exception, CustomException):
        return JsonResponse(
            data={
                "error": "A custom exception occurred",
            },
            status=400)

    # For convenience, you may want to fallback to the default exception handler
    # which will detect most exceptions that look like response errors
    # like PermissionDenied or Http404
    return default_exception_handler(request, endpoint_name, exception)

# Register the custom exception handler in settings.py
from small_view_set.config import SmallViewSetConfig

SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(
    exception_handler=app_exception_handler
)
```

With this setup, any `CustomException` raised in your endpoints will be caught by `app_exception_handler`, and a custom JSON response will be returned.
