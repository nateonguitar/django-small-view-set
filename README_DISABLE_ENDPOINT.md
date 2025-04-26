# Disabling an endpoint with a decorator

It may be useful to disable an endpoint instead of commenting it out or deleting it.

### When `SMALL_VIEW_SET_CONFIG.respect_disabled_endpoints` in Django settings is `True`

This decorator will raise an `EndpointDisabledException`, resulting in a 405 response.

### When `SMALL_VIEW_SET_CONFIG.respect_disabled_endpoints` in Django settings is `False`

The endpoint will remain active. It is useful to re-enable endpoints
when testing to maintain the functionality of the endpoint without leaving it active.

## Usage:
Apply this decorator directly to an orchestrator method or endpoint method.

Example:

```python
from small_view_set import endpoint_disabled
from urllib.request import Request

class MyViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/my_endpoint/',         self.collection, name='my_endpoint_collection'),
            path('api/my_endpoint/<int:pk>', self.detail,     name='my_endpoint_detail'),
            path('api/my_endpoint/custom',   self.custom,     name='my_endpoint_custom'),
        ]

    @endpoint(allowed_methods=['POST', 'GET'])
    def collection(self, request: Request):
        if request.method == 'POST':
            return self.create(request)
        if request.method == 'GET':
            return self.list(request)
        raise MethodNotAllowed(request.method)

    # Disable the entire collection
    @endpoint(allowed_methods=['GET'])
    @endpoint_disabled
    def detail(self, request: Request, pk: int):
        if request.method == 'GET':
            return self.retrieve(request)
        raise MethodNotAllowed(request.method)

    def create(self, request: Request):
        self.protect_create(request)
        . . .

    # Leave the rest of the collection orchestrator enabled and disable just this endpoint
    @endpoint_disabled
    def list(self, request: Request):
        self.protect_list(request)
        . . .

    def retrieve(self, request: Request):
        self.protect_retrieve(request)
        . . .

    # Disable a custom endpoint
    @endpoint(allowed_methods=['POST'])
    @endpoint_disabled
    def custom(self, request: Request)
        self.protect_create(request)
        . . .
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

is roughly equivalent to:

```python
func1(func2(test()))
```