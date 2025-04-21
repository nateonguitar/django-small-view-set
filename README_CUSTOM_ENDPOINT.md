# Custom Endpoints with Django Small View Set

This guide demonstrates how to define custom endpoints alongside the default router.

## Example Usage

Here’s how you can define a viewset with one default router endpoint and two custom endpoints:

```python
from django.http import JsonResponse
from django.urls import path
from small_view_set.decorators import default_handle_endpoint_exceptions
from small_view_set import SmallViewSet

class MyCustomViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/my_endpoint/',                 self.default_router,           name='my_endpoint_collection'),
            path('api/my_endpoint/custom/',          self.custom_collection_method, name='my_custom_collection'),
            path('api/my_endpoint/<int:pk>/custom/', self.custom_detail_method,     name='my_custom_detail'),
        ]

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Default collection endpoint"}, status=200)

    @default_handle_endpoint_exceptions
    def custom_collection_method(self, request, *args, **kwargs):
        self.protect_post(request)
        return JsonResponse({"message": "Custom collection endpoint"}, status=200)

    @default_handle_endpoint_exceptions
    def custom_detail_method(self, request, pk, *args, **kwargs):
        self.protect_update(request)
        return JsonResponse({"message": f"Custom detail endpoint for ID {pk}"}, status=200)
```

## Next Steps

- Learn about [Handling Endpoint Exceptions](./README_HANDLE_ENDPOINT_EXCEPTIONS.md) to customize error handling.
- Explore [Custom Protections](./README_CUSTOM_PROTECTIONS.md) to secure your endpoints.