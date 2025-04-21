# Registering URLs with Django Small View Set

This guide demonstrates how to register a viewset in `urls.py`.

```python
from django.http import JsonResponse
from django.urls import path
from small_view_set.small_view_set import SmallViewSet
from small_view_set.decorators import default_handle_endpoint_exceptions

class BarViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/bar/', self.default_router, name='bar_collection'),
        ]

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "bar accessed"}, status=200)
```

## Registering in `urls.py`

To register the viewset in your `urls.py`:

```python
from api.views.bar import BarViewSet

urlpatterns = [
    # Other URLs like admin, static, etc.

    *BarViewSet().urlpatterns(),
]
```