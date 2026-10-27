"""Root URL configuration of the site: home page, apps routes and admin."""
from django.contrib import admin
from django.urls import path, include
from oc_lettings_site.views import error_404, error_500

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
    path('404/', error_404, name='404'),
    path('500/', error_500, name='500'),
    path('crash/', views.crash, name='crash'),
]
