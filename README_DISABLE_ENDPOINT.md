# Disabling an endpoint with a decorator

Temporarily disables an API endpoint based on the SMALL_VIEWSET_RESPECT_DISABLED_ENDPOINTS setting.

When `SMALL_VIEWSET_RESPECT_DISABLED_ENDPOINTS` in Django settings is either not set or set to `True`, this decorator
will raise an `EndpointDisabledException`, resulting in a 404 response. When set to `False`,
the endpoint will remain active, which is useful for testing environments.

Usage:
    - Apply this decorator directly to a view method or action.
    - Example:
    
    ```python
    class ExampleViewSet(SmallViewSet):

        @default_handle_endpoint_exceptions
        @disable_endpoint
        def retrieve(self, request: Request) -> JsonResponse:
            self.protect_retrieve(request)
            . . .
    ```

# IMPORTANT

The `@disable_endpoint` decorator must be after the exception handler decorator for the disabled endpoint thrown error to be caught

- Good
    ```
    @default_handle_endpoint_exceptions
    @disable_endpoint
    ```
- Bad
    ```
    @disable_endpoint
    @default_handle_endpoint_exceptions
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