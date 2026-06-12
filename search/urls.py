from django.urls import path

from . import views

urlpatterns = [
    path("", views.page, name="search-base"),
    path("?{{ request.GET.urlencode }}", views.page, name="search"),
]