from django.http import JsonResponse
from django.urls import path
from urllib.request import Request
from small_view_set import endpoint, SmallViewSet

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

class DefaultRouterViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/default_router/',          self.default_router, name='default_router_collection'),
            path('api/default_router/<int:pk>/', self.default_router, name='default_router_details'),
        ]

    @endpoint(allowed_methods=['GET'])
    async def list(self, request):
        return JsonResponse({"value": 1}, status=200)

    @endpoint(allowed_methods=['POST'])
    def create(self, request):
        return JsonResponse({"value": 2}, status=201)

    @endpoint(allowed_methods=['GET'])
    def retrieve(self, request, pk):
        return JsonResponse({"value": 3}, status=200)

    @endpoint(allowed_methods=['PUT'])
    def put(self, request, pk):
        return JsonResponse({"value": 4}, status=200)

    @endpoint(allowed_methods=['DELETE'])
    def delete(self, request, pk):
        return JsonResponse(None, safe=False, status=204)
