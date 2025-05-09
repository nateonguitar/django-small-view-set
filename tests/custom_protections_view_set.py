from django.http import JsonResponse
from django.urls import path
from urllib.request import Request

from small_view_set import SmallViewSet, endpoint, Unauthorized
from small_view_set.exceptions import MethodNotAllowed


class AppViewSet(SmallViewSet):

    def require_logged_in(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise Unauthorized("Authorization header is missing")


    def require_email_verified(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise Unauthorized("Authorization header is missing")
        if auth_header == 'Bearer logged_in_but_not_verified':
            raise Unauthorized("User is logged in but not verified")

    def protect_create(
        self,
        request: Request,
        require_logged_in=True,
        require_email_verified=True):
        super().protect_create(request)
        if require_logged_in:
            self.require_logged_in(request)
        if require_email_verified:
            self.require_email_verified(request)

    def protect_list(
        self,
        request: Request,
        require_logged_in=True,
        require_email_verified=True):
        super().protect_list(request)
        if require_logged_in:
            self.require_logged_in(request)
        if require_email_verified:
            self.require_email_verified(request)

    def protect_retrieve(
        self,
        request: Request,
        require_logged_in=True,
        require_email_verified=True):
        super().protect_retrieve(request)
        if require_logged_in:
            self.require_logged_in(request)
        if require_email_verified:
            self.require_email_verified(request)

    def protect_update(
        self,
        request: Request,
        require_logged_in=True,
        require_email_verified=True):
        super().protect_update(request)
        if require_logged_in:
            self.require_logged_in(request)
        if require_email_verified:
            self.require_email_verified(request)

    def protect_delete(
        self,
        request: Request,
        require_logged_in=True,
        require_email_verified=True):
        super().protect_delete(request)
        if require_logged_in:
            self.require_logged_in(request)
        if require_email_verified:
            self.require_email_verified(request)



class CustomProtectionsViewSet(AppViewSet):
    def urlpatterns(self):
        return [
            path('api/custom_protections/',          self.collection, name='custom_protections_collection'),
            path('api/custom_protections/<int:pk>/', self.detail,     name='custom_protections_detail'),
        ]

    @endpoint(allowed_methods=['POST'])
    def collection(self, request: Request):
        if request.method == 'POST':
            return self.create(request)
        raise MethodNotAllowed(method=request.method)

    @endpoint(allowed_methods=['GET'])
    def detail(self, request: Request, pk: int):
        if request.method == 'GET':
            return self.retrieve(request, pk)
        raise MethodNotAllowed(method=request.method)

    def create(self, request: Request):
        self.protect_create(request)
        return JsonResponse({'name': 'Created'})

    def retrieve(self, request: Request, pk: int):
        self.protect_retrieve(request)
        return JsonResponse({'id': pk, 'name': 'Retrieved'})