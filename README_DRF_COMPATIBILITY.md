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

Define some throttles, like this `throttles.py`
```python
from django.core.cache import cache
from django.conf import settings
from rest_framework.exceptions import Throttled
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle


def get_client_ip(request: Request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class _EndpointThrottle(SimpleRateThrottle):
    throttle_cache_key_prefix = 'throttle|generic_'

    def get_cache_key(self, request, view):
        identifier: str
        if request.user and request.user.is_authenticated:
            identifier = f'user_{request.user.id}'
        else:
            ip = get_client_ip(request)
            identifier = f'ip_{ip}'
        return self.throttle_cache_key_prefix + identifier

    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        if not allowed:
            wait = self.wait()
            raise Throttled(wait=wait)
        return allowed

class EndpointReadThrottle(_EndpointThrottle):
    rate = '20/minute'
    throttle_cache_key_prefix = 'throttle|read_'


class EndpointWriteThrottle(_EndpointThrottle):
    rate = '1/minute'
    throttle_cache_key_prefix = 'throttle|write_'

```

```python
from api.throttling import EndpointReadThrottle, EndpointWriteThrottle
from rest_framework.exceptions import Throttled
from small_view_set import Unauthorized

from api.app_view_set import AppViewSet

class ThrottledItemsViewSet(AppViewSet):
    read_throttle = EndpointReadThrottle()
    write_throttle = EndpointWriteThrottle()

    def protect_create(self, request, apply_throttle=True):
        super().protect_create(request)
        if apply_throttle:
            # In this configuration, checking allow_reqeuest will throw a Throttled exception if not allowed
            write_throttle.allow_request(request, None)

    def protect_list(self, request, apply_throttle=True):
        super().protect_list(request)
        if apply_throttle:
            read_throttle.allow_request(request, None)

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
        self.protect_list(request, apply_throttle=False)
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
from rest_framework import serializers as drf_serializers
from rest_framework import exceptions as drf_exceptions
from small_view_set import default_exception_handler

def app_exception_handler(request: Request, endpoint_name: str, exception):
    try:
        raise exception

    except drf_serializers.ValidationError as e:
        logger.error(f"Validation error in {endpoint_name}: {e}")
        return JsonResponse(e.detail, status=400)

    except drf_exceptions.Throttled as e:
        msg = f"You must wait {e.wait} seconds before trying again." if e.wait else "Too many requests"
        return JsonResponse(msg, safe=False, status=e.status_code)

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
