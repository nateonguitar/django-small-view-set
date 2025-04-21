# Custom Protections with Django Small View Set

This guide explains how to subclass `SmallViewSet` to add custom protections.

## Example: Logged-In Protection

Here’s how to add a logged-in protection:

```python
from small_view_set import SmallViewSet
from small_view_set.decorators import default_handle_endpoint_exceptions
from small_view_set.exceptions import Unauthorized

class AppViewSet(SmallViewSet):

    def require_logged_in(self, request):
        if not request.user or not request.user.is_authenticated:
            raise Unauthorized()

    # User is required to be logged in to create by default
    def protect_create(self, request, require_logged_in=True):
        super().protect_create(request)
        if require_logged_in:
            self.require_logged_in(request)

    # User is NOT required to be logged in to view by default
    def protect_list(self, request, require_logged_in=False):
        super().protect_list(request)
        if require_logged_in:
            self.require_logged_in(request)

class MyProtectedViewSet(AppViewSet):

    def urlpatterns(self):
        return [
            path('api/protected/', self.default_router, name='protected_collection'),
        ]

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "This is a protected endpoint!"}, status=200)

    @default_handle_endpoint_exceptions
    def create(self, request, *args, **kwargs):
        self.protect_create(request)
        # Or to skip
        self.protect_create(request, require_logged_in=False)

        return JsonResponse({"message": "Protected resource created!"}, status=201)
```

## Next Steps

- Check out [Handling Endpoint Exceptions](./README_HANDLE_ENDPOINT_EXCEPTIONS.md) to customize error handling.
- Explore [Getting Started](./README_SIMPLE.md) for a basic example.