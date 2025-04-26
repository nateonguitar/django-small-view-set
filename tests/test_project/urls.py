from tests.custom_endpoints_view_set import CustomEndpointsViewSet
from tests.basic_crud_view_set import BasicCrudViewSet
from tests.custom_protections_view_set import CustomProtectionsViewSet

urlpatterns = [
    *CustomEndpointsViewSet().urlpatterns(),
    *CustomProtectionsViewSet().urlpatterns(),
    *BasicCrudViewSet().urlpatterns(),
]