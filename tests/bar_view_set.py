import asyncio
from django.http import JsonResponse, Http404
from django.urls import path

from small_view_set.decorators import (
    default_handle_endpoint_exceptions,
    disable_endpoint,
)
from small_view_set.small_view_set import SmallViewSet

class BarViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/bar/',               self.collection,    name='bar_collection'),
            path('api/bar/some-endpoint/', self.some_endpoint, name='bar_some_endpoint'),
            path('api/bar/dog/',           self.dog,           name='bar_dog'),
            path('api/bar/cat/',           self.cat,           name='bar_cat'),
            path('api/bar/<int:pk>/',      self.detail,        name='bar_detail'),
        ]

    @default_handle_endpoint_exceptions
    def collection(self, request):
        self.protect_create(request)
        return JsonResponse(data=None, safe=False, status=200)

    @default_handle_endpoint_exceptions
    def detail(self, request, pk):
        self.protect_update(request)
        if pk == 1:
            raise Http404()
        return JsonResponse(data=None, safe=False, status=200)

    @default_handle_endpoint_exceptions
    @disable_endpoint
    def some_endpoint(self, request):
        self.protect_retrieve(request)
        return JsonResponse(data=None, safe=False, status=200)

    @default_handle_endpoint_exceptions
    async def dog(self, request):
        self.protect_list(request)
        await asyncio.sleep(1)
        return JsonResponse(data=None, safe=False, status=200)

    @default_handle_endpoint_exceptions
    @disable_endpoint
    async def cat(self, request):
        await asyncio.sleep(1)
        return JsonResponse(data=None, safe=False, status=200)