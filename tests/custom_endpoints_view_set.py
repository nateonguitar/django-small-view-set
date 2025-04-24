import asyncio
from django.http import JsonResponse, Http404
from django.urls import path
from urllib.request import Request

from small_view_set import endpoint, endpoint_disabled, SmallViewSet


class AppViewSet(SmallViewSet):
    def protect_create(self, request: Request):
        super().protect_create(request)

    def protect_list(self, request: Request):
        super().protect_list(request)

    def protect_retrieve(self, request: Request):
        super().protect_retrieve(request)

    def protect_update(self, request: Request):
        super().protect_update(request)

    def protect_delete(self, request: Request):
        super().protect_delete(request)


class CustomEndpointsViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/custom_endpoints/',                 self.collection,               name='custom_collection'),
            path('api/custom_endpoints/<int:pk>/',        self.detail,                   name='custom_detail'),
            path('api/custom_endpoints/some-endpoint/',   self.some_endpoint,            name='custom_some_endpoint'),
            path('api/custom_endpoints/dog/',             self.dog,                      name='custom_dog'),
            path('api/custom_endpoints/cat/',             self.cat,                      name='custom_cat'),
            path('api/custom_endpoints/custom/',          self.collection_get,           name='custom_collection_get'),
            path('api/custom_endpoints/<int:pk>/custom/', self.detail_put,               name='custom_detail_put'),
        ]

    @endpoint(allowed_methods=['POST'])
    def collection(self, request):
        return JsonResponse(data=None, safe=False, status=200)

    @endpoint(allowed_methods=['PUT', 'PATCH'])
    def detail(self, request, pk):
        if pk == 1:
            raise Http404()
        return JsonResponse(data=None, safe=False, status=200)

    @endpoint(allowed_methods=['GET'])
    @endpoint_disabled
    def some_endpoint(self, request):
        return JsonResponse(data=None, safe=False, status=200)

    @endpoint(allowed_methods=['GET'])
    async def dog(self, request):
        await asyncio.sleep(1)
        return JsonResponse(data=None, safe=False, status=200)

    @endpoint(allowed_methods=['GET'])
    @endpoint_disabled
    async def cat(self, request):
        await asyncio.sleep(1)
        return JsonResponse(data=None, safe=False, status=200)

    @endpoint(allowed_methods=['GET'])
    def collection_get(self, request):
        return JsonResponse({"value": 6}, status=200)

    @endpoint(allowed_methods=['PUT'])
    def detail_put(self, request, pk):
        return JsonResponse({"value": 7}, status=200)