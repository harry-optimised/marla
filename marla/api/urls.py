from django.urls import path
from .views import ask_question, update_context

urlpatterns = [
    path("ask/", ask_question, name="ask"),
    path("update_context/", update_context, name="update-context"),
]
