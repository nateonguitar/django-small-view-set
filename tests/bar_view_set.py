from django.http import JsonResponse, Http404
from django.urls import path

from small_view_set.decorators import default_handle_endpoint_exceptions
from small_view_set.small_view_set import SmallViewSet

1

class BarViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/bar/',                 self.collection, name='bar_collection'),
            path('api/bar/<int:pk>/',        self.detail,     name='bar_detail'),
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
