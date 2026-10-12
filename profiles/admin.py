"""Admin registration of the profiles app models."""
from django.contrib import admin

from .models import Profile

admin.site.register(Profile)
