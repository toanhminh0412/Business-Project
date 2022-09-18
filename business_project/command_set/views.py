from django.shortcuts import render
from django.views.generic.list import ListView
from .models import CommandSet

# Create your views here.
class HomePageView(ListView):
    model = CommandSet
    template_name = "command_set/homepage.html"
    context_object_name = "command_sets"