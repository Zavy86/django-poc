from django.contrib import admin
from django.urls import path

from poc.views import index

from .views import welcome

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome, name="welcome"),
    path("poc", index, name="index"),
]
