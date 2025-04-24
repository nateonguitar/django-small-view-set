# Disabling an endpoint with a decorator

Temporarily disables an API endpoint based on the SMALL_VIEW_SET_CONFIG setting.

When `SMALL_VIEW_SET_CONFIG.respect_disabled_endpoints` in Django settings is either not set or set to `True`, this decorator
will raise an `EndpointDisabledException`, resulting in a 404 response. When set to `False`,
the endpoint will remain active, which is useful for testing environments.

Usage:
    - Apply this decorator directly to a view method or action.
    - Example:

    ```python
    from small_view_set.decorators import endpoint_disabled
    from small_view_set.config import SmallViewSetConfig

    # Register SmallViewSetConfig in settings
    SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()

    class ExampleViewSet(SmallViewSet):

        @endpoint(allowed_methods=['GET'])
        @endpoint_disabled
        def retrieve(self, request, *args, **kwargs):
            self.protect_retrieve(request)
            return JsonResponse({"message": "This endpoint is disabled."})
    ```

# IMPORTANT

The `@endpoint_disabled` decorator must be after the `@endpoint` decorator for the disabled endpoint thrown error to be caught.

- Good
    ```
    @endpoint(allowed_methods=['GET'])
    @endpoint_disabled
    ```
- Bad
    ```
    @endpoint_disabled
    @endpoint(allowed_methods=['GET'])
    ```

This is just how decorators work in python. The first decorator wraps the second, second wraps the third, and so on.

Given:
```python
@func1
@func2
def test:
    pass
```

When running:
```
test()
```

is equivalent to:

```python
func1(func2(test()))
```