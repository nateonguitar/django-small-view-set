# Getting Started with Django Small View Set

This guide provides a simple example to get started with the library.

## Example Usage

Here’s how you can define a basic API endpoint with one collection route and one detail route:

```python
from django.http import JsonResponse
from django.urls import path
from small_view_set.small_view_set import SmallViewSet
from small_view_set.decorators import default_handle_endpoint_exceptions

class MyViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/my_endpoint/', self.default_router, name='my_endpoint_collection'),
            path('api/my_endpoint/<int:pk>/', self.default_router, name='my_endpoint_detail'),
        ]

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)

    @default_handle_endpoint_exceptions
    def retrieve(self, request, pk, *args, **kwargs):
        self.protect_retrieve(request)
        return JsonResponse({"message": f"Detail for ID {pk}"}, status=200)
```

## Next Steps

- Explore [Custom Endpoints](./README_CUSTOM_ENDPOINT.md) to learn how to define additional routes.
- Check out [Handling Endpoint Exceptions](./README_HANDLE_ENDPOINT_EXCEPTIONS.md) for error handling strategies.