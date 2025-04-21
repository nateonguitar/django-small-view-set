# Using Django Rest Framework (DRF) Tools with Small View Set

This guide demonstrates how to integrate DRF tools like serializers and throttles with the Small View Set library.

## Example: Using DRF Serializers

You can use DRF serializers for validation and serialization while defining your API logic explicitly in the viewset methods. Here’s an example:

```python
from django.http import JsonResponse
from django.urls import path
from rest_framework import serializers

from small_view_set.decorators import default_handle_endpoint_exceptions
from small_view_set.small_view_set import SmallViewSet

class FooCreateValidator(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()

class FooReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Foo
        fields = (
            'id',
            'user',
            'name',
            'age',
            'created_at',
            'updated_at',
        )

class FooViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/foo/', self.default_router, name='foo_collection'),
        ]

    @default_handle_endpoint_exceptions
    def create(self, request, *args, **kwargs):
        self.protect_create(request)
        request_user: User = request.user
        data = self.parse_json_body(request)

        # Use the DRF serializer for validation
        validator = FooCreateValidator(data=data)
        validator.is_valid(raise_exception=True)

        validated_data = validator.validated_data.copy()
        foo = Foo.objects.create(
            **validated_data,
            user=request_user,
        )

        # Use a DRF model serializer for response data
        serializer = FooReadSerializer(foo)
        return JsonResponse(serializer.data, status=201)
```

## Example: Using DRF Throttles

You can also use DRF throttling classes to limit the rate of requests to your endpoints. Here’s an example:

```python
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled
from small_view_set import SmallViewSet
from small_view_set.exceptions import Unauthorized

class ThrottledViewSet(SmallViewSet):

    def protect_create(self, request, apply_throttles=True):
        super().protect_create(request)

        # Apply DRF throttling
        if apply_throttles:
            throttle = UserRateThrottle()
            if not throttle.allow_request(request, None):
                # The default exeption handler will duck-type DRF's exceptions,
                # or you can catch Throttled in your own custom exception handler decorator
                raise Throttled(detail=throttle.wait)

    def urlpatterns(self):
        return [
            path('api/throttled/', self.default_router, name='throttled_collection'),
        ]

    @default_handle_endpoint_exceptions
    def create(self, request, *args, **kwargs):
        self.protect_create(request)
        return JsonResponse({"message": "Throttled endpoint accessed"}, status=201)
```

## Why Use DRF Tools with Small View Set?

- **Validation**: DRF serializers provide robust validation and transformation for your data.
- **Throttling**: DRF throttling classes allow you to control the rate of requests to your endpoints.
- **Compatibility**: Small View Set is designed to work seamlessly with DRF tools, giving you the best of both worlds.

## Next Steps

- Check out [Getting Started](./README_SIMPLE.md) for a basic example.
- Explore [Custom Protections](./README_CUSTOM_PROTECTIONS.md) to secure your endpoints.