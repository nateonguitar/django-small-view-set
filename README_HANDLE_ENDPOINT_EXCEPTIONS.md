# Handling Endpoint Exceptions

This guide explains how to handle exceptions in your endpoints and customize the behavior.

## Using the Default Decorator

The library provides a `default_handle_endpoint_exceptions` decorator to handle common API errors gracefully. Here’s an example:

```python
from small_view_set import SmallViewSet
from small_view_set.decorators import default_handle_endpoint_exceptions

class MyViewSet(SmallViewSet):

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)
```

## Writing Your Own Decorator

The `@default_handle_endpoint_exceptions` is not intended to be used for production apps, though it technically could handle it. It is named a little long to pressure developers to write their own handler.

You can write your own decorator by copying the `default_handle_endpoint_exceptions` implementation and customizing it for your app. For example:

```python
from django.http import JsonResponse

def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return wrapper
```

Then use it in your viewset:

```python
class MyViewSet(SmallViewSet):

    @exception_handler
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)
```

## Next Steps

- Explore [Custom Protections](./README_CUSTOM_PROTECTIONS.md) to secure your endpoints.
- Check out [Getting Started](./README_SIMPLE.md) for a basic example.