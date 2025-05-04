# Using Django Rest Framework (DRF) Tools with Small View Set

This guide demonstrates how to integrate DRF tools like serializers and throttles

## Example: Using DRF Serializers

You can use DRF serializers for validation and serialization while defining your API logic explicitly in the viewset methods.

Keep in mind, the point of this pattern is to remove black-box behaviors and maintain separation of concerns,
so do not use serializer methods like `create` or `update`. There's really nothing stopping you, but 
this guide values the separation.

```python
from django.http import JsonResponse
from django.urls import path
from rest_framework import serializers
from small_view_set import endpoint
from urllib.request import Request

from api.app_view_set import AppViewSet

class FooCreateValidator(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()


class FooReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Foo
        fields = ('id', 'name', 'age', 'created_at', 'updated_at')


class FooViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/foo/', self.collection, name='foo_collection'),
        ]

    @endpoint(allowed_methods=['POST'])
    def collection(self, request: Request):
        if request.method == 'POST':
            return self.create(request)
        raise MethodNotAllowed(request.method)

    def create(self, request: Request):
        self.protect_create(request)
        data = self.parse_json_body(request)

        # Use the DRF serializer for validation
        validator = FooCreateValidator(data=data)
        validator.is_valid(raise_exception=True)

        # If your validated_data has keys that match your model,
        # you can flatten it into the create method with **
        foo = Foo.objects.create(
            **validator.validated_data,
            user=request.user)

        # Use a DRF model serializer for response data
        serializer = FooReadSerializer(foo)
        return JsonResponse(serializer.data, status=201)
```

## Example: Using DRF Throttles

You can also use DRF throttling classes to limit the rate of requests to your endpoints. Here’s an example:

```python
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled
from small_view_set import Unauthorized

from api.app_view_set import AppViewSet

class ThrottledItemsViewSet(AppViewSet):
    def protect_create(self, request, apply_throttles=True):
        super().protect_create(request)

        if apply_throttles:
            throttle = UserRateThrottle()
            if not throttle.allow_request(request, None):
                # The default exeption handler will duck-type DRF's exceptions,
                # or you can catch Throttled in your own custom exception handler
                raise Throttled(detail=throttle.wait)

    def urlpatterns(self):
        return [
            path('api/throttle_items/', self.collection, name='throttled_items_collection'),
        ]

    @endpoint(allowed_methods=['POST', 'GET'])
    def collection(self, request: Request):
        if request.method == 'POST':
            return self.create(request)
        if request.method == 'GET':
            return self.list(request)
        raise MethodNotAllowed(request.method)

    def create(self, request):
        self.protect_create(request)
        return JsonResponse({"message": "Throttled endpoint accessed"}, status=201)

    def list(self, request):
        self.protect_list(request, apply_throttles=False)
        return JsonResponse({"message": "This endpoint is not rate throttled"}, status=200)
```

## DRF Exception Handling

A lot of DRF exceptions will just work with the default exception handler, but validation errors thrown from serializer validation will just say "Bad Request" unless handled.

```python
# Some endpoint code:
validator = FooCreateValidator(data=data)
validator.is_valid(raise_exception=True)
```

Catching the exception thrown by `raise_exception=True` when the validation does not pass:
```python
from django.http import JsonResponse
from urllib.request import Request
from small_view_set import default_exception_handler

# Note: django also has a ValidationError for form errors:
#   from django.core.exceptions import ValidationError
# Be careful to catch DRF's exception specifically
from rest_framework import serializers as drf_serializers

def app_exception_handler(request: Request, endpoint_name: str, exception):
    try:
        raise exception
    except drf_serializers.ValidationError as e:
        return JsonResponse(e.detail, status=400)
    except Exception as e:
        return default_exception_handler(request, endpoint_name, exception)
```

And don't forget to register SmallViewSetConfig in settings.py with your app's exception handler
```python
SMALL_VIEW_SET_CONFIG = SmallViewSetConfig(
    exception_handler=app_exception_handler)
```

## Why Use DRF Tools with Small View Set?

- **Validation**: DRF serializers provide robust validation and transformation for your data.
- **Throttling**: DRF throttling classes allow you to control the rate of requests to your endpoints.
- **Compatibility**: Small View Set is designed to work seamlessly with DRF tools, giving you the best of both worlds.
