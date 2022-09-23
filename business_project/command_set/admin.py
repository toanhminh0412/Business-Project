from django.contrib import admin
from .models import CommandSet, Tool, WordIndex, UserProfile

# Register your models here.
admin.site.register(CommandSet)
admin.site.register(Tool)
admin.site.register(WordIndex)
admin.site.register(UserProfile)