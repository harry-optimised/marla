from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("settings/", views.settings, name="settings"),
    path("account/", views.account, name="account"),
    path("integrations/", views.integrations, name="integrations"),
]
