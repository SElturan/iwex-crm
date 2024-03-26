from django.urls import path
from .endoint import views, auth_views


urlpatterns = [
    path('auth/', auth_views.google_login),
    path('google/', auth_views.google_auth),
]
