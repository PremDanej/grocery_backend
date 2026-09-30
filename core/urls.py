from django.contrib import admin
from django.urls import include, path

ROOT_PATH = "api/v1/"
urlpatterns = [
    path("admin/", admin.site.urls),
    path(ROOT_PATH + "catalog/", include("catalog.urls")),
    path(ROOT_PATH + "users/", include("users.urls")),
    path(ROOT_PATH + "orders/", include("orders.urls")),
]
