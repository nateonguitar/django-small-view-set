# Custom Endpoints with Django Small View Set

This guide demonstrates how to define custom endpoints alongside the default router.

## Example Usage

Here’s how you can define a viewset with one default router endpoint and two custom endpoints:

```python
from django.http import JsonResponse
from django.urls import path
from small_view_set.decorators import endpoint
from small_view_set.config import SmallViewSetConfig

# Register SmallViewSetConfig in settings
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()

class MyCustomViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/my_endpoint/',                 self.default_router,           name='my_endpoint_collection'),
            path('api/my_endpoint/custom/',          self.custom_collection_method, name='my_custom_collection'),
            path('api/my_endpoint/<int:pk>/custom/', self.custom_detail_method,     name='my_custom_detail'),
        ]

    @endpoint(allowed_methods=['GET'])
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Default collection endpoint"}, status=200)

    @endpoint(allowed_methods=['POST'])
    def custom_collection_method(self, request, *args, **kwargs):
        self.protect_create(request)
        return JsonResponse({"message": "Custom collection endpoint"}, status=200)

    @endpoint(allowed_methods=['PUT'])
    def custom_detail_method(self, request, pk, *args, **kwargs):
        self.protect_update(request)
        return JsonResponse({"message": f"Custom detail endpoint for ID {pk}"}, status=200)
```
