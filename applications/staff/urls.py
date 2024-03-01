from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'interviews', InterviewsModelViewsets, basename='interviews')

urlpatterns = [
  # сотрудники
  path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
  path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
  # profiles
  path('profile/<int:pk>/', StaffProfileAPIView.as_view(), name='staff_profile_api'),
  path('profile-detail/<int:pk>/', GetAllProfileDetail.as_view(), name='profile-detail'),
  # vacancies
  path('all-vacancies/', GetAllVacanciesAPIView.as_view(), name='all-vacancies'),
  path('vacancies-detail/<int:pk>/', GetAllVacanciesDetail.as_view(), name='vacancies-detail'),
  path('vacancies/<int:pk>/add_student/', AddStudentToVacancyAPIView.as_view(), name='add_student_to_vacancy'),
  # employer
  path('employer/profiles/', EmployerProfileListAPIView.as_view(), name='employer-profile-list'),
  path('employer/company/', EmployerCompanyAPIView.as_view(), name='employer-company'),
  path('employer/company/update/', EmployerCompanyUpdateView.as_view(), name='employer-company-update'),
  # favorite
  path('favorites/', FavoriteListAPIView.as_view(), name='favorite-list'),
  path('favorite/', FavoriteAPIView.as_view(), name='favorite-create'),
  # interviews
  path('interviews/', InterviewsAPIView.as_view(), name='interviews-create'),
  # orders
  path('order-students/<int:pk>/', OrderStudentsDetailView.as_view(), name='order-students-detail'),

  
]