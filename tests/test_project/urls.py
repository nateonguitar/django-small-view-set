from tests.custom_endpoints_view_set import CustomEndpointsViewSet
from tests.default_router_view_set import DefaultRouterViewSet
from tests.custom_protections_view_set import CustomProtectionsViewSet

urlpatterns = [
    *CustomEndpointsViewSet().urlpatterns(),
    *CustomProtectionsViewSet().urlpatterns(),
    *DefaultRouterViewSet().urlpatterns(),
]