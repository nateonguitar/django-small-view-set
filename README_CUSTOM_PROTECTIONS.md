# Custom Protections with Django Small View Set

This guide explains how to subclass `SmallViewSet` to add custom protections.

## Example: Logged-In Protection

Here’s how to add a logged-in protection:

```python
from small_view_set import (
    SmallViewSet,
    SmallViewSetConfig,
    Unauthorized,
    endpoint,
)

# Register SmallViewSetConfig in settings
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()

class AppViewSet(SmallViewSet):
    def require_logged_in(self, request):
        if not request.user or not request.user.is_authenticated:
            raise Unauthorized()

    # User is required to be logged in to create (unless bypassed)
    def protect_create(self, request, require_logged_in=True):
        super().protect_create(request)
        if require_logged_in:
            self.require_logged_in(request)

    # User is NOT required to be logged in to view the list (unless bypassed)
    def protect_list(self, request, require_logged_in=False):
        super().protect_list(request)
        if require_logged_in:
            self.require_logged_in(request)

class MyProtectedViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/protected/', self.default_router, name='protected_collection'),
        ]

    @endpoint(allowed_methods=['POST'])
    def create(self, request, *args, **kwargs):
        self.protect_create(request)
        return JsonResponse({"message": "Protected resource created!"}, status=201)

    @endpoint(allowed_methods=['GET'])
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "This is a protected endpoint!"}, status=200)
```
