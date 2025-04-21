from tests.bar_view_set import BarViewSet
from tests.foo_view_set import FooViewSet

urlpatterns = [
    *BarViewSet().urlpatterns(),
    *FooViewSet().urlpatterns(),
]