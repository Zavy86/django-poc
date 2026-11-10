from django.contrib import admin
from django.urls import path

from __APP_NAME__.views import index

from .views import welcome

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome, name="welcome"),
    path("__APP_NAME__", index, name="index"),
]
