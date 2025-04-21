from django.http import JsonResponse
from django.urls import path

from small_view_set.decorators import default_handle_endpoint_exceptions
from small_view_set.small_view_set import SmallViewSet

1

class FooViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/foo/',                 self.default_router,           name='foo_collection'),
            path('api/foo/<int:pk>/',        self.default_router,           name='foo_details'),
            path('api/foo/custom/',          self.custom_collection_method, name='foo_custom'),
            path('api/foo/<int:pk>/custom/', self.custom_detail_method,     name='foo_custom_detail'),
        ]

    @default_handle_endpoint_exceptions
    async def list(self, request):
        self.protect_list(request)
        return JsonResponse({"value": 1}, status=200)

    @default_handle_endpoint_exceptions
    def create(self, request):
        self.protect_create(request)
        return JsonResponse({"value": 2}, status=201)

    @default_handle_endpoint_exceptions
    def retrieve(self, request, pk):
        self.protect_retrieve(request)
        return JsonResponse({"value": 3}, status=200)

    @default_handle_endpoint_exceptions
    def put(self, request, pk):
        self.protect_update(request)
        return JsonResponse({"value": 4}, status=200)

    @default_handle_endpoint_exceptions
    def delete(self, request, pk):
        self.protect_delete(request)
        return JsonResponse(None, safe=False, status=204)

    @default_handle_endpoint_exceptions
    def custom_collection_method(self, request):
        self.protect_list(request)
        return JsonResponse({"value": 6}, status=200)

    @default_handle_endpoint_exceptions
    def custom_detail_method(self, request, pk):
        self.protect_update(request)
        return JsonResponse({"value": 7}, status=200)
