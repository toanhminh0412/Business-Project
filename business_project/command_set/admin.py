from django.contrib import admin
from .models import CommandSet, Tool, WordIndex

# Register your models here.
admin.site.register(CommandSet)
admin.site.register(Tool)
admin.site.register(WordIndex)