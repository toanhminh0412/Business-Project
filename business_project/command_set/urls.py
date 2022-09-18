from django.urls import path
from .views import HomePageView

from . import views

urlpatterns = [
    path("", view=HomePageView.as_view(), name="command_set_homepage"),
]