from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import CartItemViewSet, OrderViewSet, UserAddressViewSet

router = DefaultRouter()
router.register(r"addresses", UserAddressViewSet, basename="address")
router.register(r"cart", CartItemViewSet, basename="cart")
router.register(r"checkout", OrderViewSet, basename="order")

urlpatterns = [path("", include(router.urls))]
