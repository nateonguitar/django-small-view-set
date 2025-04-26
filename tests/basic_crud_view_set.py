from django.http import JsonResponse
from django.urls import path
from urllib.request import Request
from small_view_set import endpoint, SmallViewSet
from small_view_set.exceptions import MethodNotAllowed

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

class BasicCrudViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/basic_crud/',          self.collection, name='basic_crud_collection'),
            path('api/basic_crud/<int:pk>/', self.detail,     name='basic_crud_details'),
        ]
    
    @endpoint(allowed_methods=['GET', 'POST'])
    async def collection(self, request):
        if request.method == 'POST':
            return await self.create(request)
        if request.method == 'GET':
            return await self.list(request)
        raise MethodNotAllowed(method=request.method)

    @endpoint(allowed_methods=['GET', 'PUT', 'DELETE'])
    def detail(self, request, pk):
        if request.method == 'GET':
            return self.retrieve(request, pk)
        if request.method == 'PUT':
            return self.put(request, pk)
        if request.method == 'DELETE':
            return self.delete(request, pk)
        raise MethodNotAllowed(method=request.method)

    async def list(self, request):
        self.protect_list(request)
        return JsonResponse({"value": 1}, status=200)

    async def create(self, request):
        self.protect_create(request)
        return JsonResponse({"value": 2}, status=201)

    def retrieve(self, request, pk):
        self.protect_retrieve(request)
        return JsonResponse({"value": 3}, status=200)

    def put(self, request, pk):
        self.protect_update(request)
        return JsonResponse({"value": 4}, status=200)

    def delete(self, request, pk):
        self.protect_delete(request)
        return JsonResponse(None, safe=False, status=204)
