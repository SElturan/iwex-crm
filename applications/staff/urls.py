from django.urls import include, path

from .views import *

urlpatterns = [
   path('staff-profile/<int:pk>/', StaffProfileAPIView.as_view(), name='staff_profile_api'),
]