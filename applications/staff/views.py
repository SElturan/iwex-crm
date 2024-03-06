from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from ..accounts.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListAPIView)
from applications.core.permissions import IsEmployerPermission
from rest_framework import generics, status
# from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import  MultiPartParser
from .permissions import IsEmployeePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView





class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class StaffProfileAPIView(generics.RetrieveAPIView):
    serializer_class = StaffProfileSerializer
    def get_queryset(self):
        profile_id = self.kwargs['pk']
        queryset = Profile.objects.filter(id=profile_id)
        return queryset

    def get(self, request, *args, **kwargs):
        profile_instance = self.get_object()
        serializer = self.get_serializer(profile_instance)
        return Response(serializer.data)


class InterviewsModelViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = StaffInterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vacancy',]


    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Interviews.objects.filter(employer__user__id=user_id).select_related('vacancy', 'user',)
        return queryset

class InterviewsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = StaffInterviewsSerializers
    parser_classes = [MultiPartParser]



    # @swagger_auto_schema(request_body=StaffInterviewsSerializers)
    def post(self, request, *args, **kwargs):
        serializer = StaffInterviewsSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get('vacancy')
            user = request.data.get('user')
            invitation = Interviews.objects.filter(employer__user__id=user_id).filter(vacancy=vacancy).filter(user=user).first()
            if invitation is not None:
                return Response({'error': 'You have already invited this applicant'}, status=status.HTTP_400_BAD_REQUEST)
            user = EmployerCompany.objects.get(user__id=user_id)
            vacancy = Vacancy.objects.filter(employer_company=user).filter(id=vacancy).first()
            if vacancy is None:
                return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(employer=user, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = StaffFavoriteListSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Favorite.objects.filter(employer__user__id=user_id).select_related('user',)
        return queryset
    


class FavoriteAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = StaffFavoriteSerializers
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        user = request.data.get('user')
        
        # Проверяем, не добавлен ли уже этот пользователь в избранное
        if Favorite.objects.filter(employer__user__id=user_id, user=user).exists():
            return Response({'error': 'You have already added this user to favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем работодателя и сохраняем в избранное
        employer = EmployerCompany.objects.get(user__id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=employer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        favorite_id = kwargs.get('pk')
        try:
            favorite = Favorite.objects.get(id=favorite_id, employer__user__id=user_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite does not exist or you do not have permission to delete it'}, status=status.HTTP_404_NOT_FOUND)

class OrderStudentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaffOrderStudentsSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    parser_classes = [MultiPartParser]
    queryset = OrderStudents.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class GetAllVacanciesAPIView(generics.ListAPIView):
    serializer_class = StaffVacanciesSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    description = "Список всех вакансий"


    def get_queryset(self):
        queryset = Vacancy.objects.all()
        employer_id = self.request.query_params.get('employer_company_id')

        if employer_id:
            queryset = queryset.filter(employer_company_id=employer_id)
        
        return queryset


class GetAllVacanciesDetail(generics.RetrieveAPIView):
    serializer_class = StaffVacanciesSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    description = "Информация о конкретной вакансии"

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        employer_id = self.request.query_params.get('employer_company_id')

        if employer_id:
            queryset = queryset.filter(employer_company_id=employer_id)
        
        return queryset
    
class AddStudentToVacancyAPIView(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = StaffVacanciesSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    description = "Добавление студента к вакансии"

    def patch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Вы не авторизованы для выполнения этого действия")
        
        vacancy = self.get_object()

        if not vacancy.active:
            return Response({"message": "Вакансия неактивна"}, status=status.HTTP_200_OK)
        
        if vacancy.add_student:
            return Response({"message": "Нет доступных рабочих мест в вакансии"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllProfileDetail(generics.RetrieveAPIView):
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    description = "Информация о конкретном профиле"

    def get_queryset(self):
        queryset = Profile.objects.all()
        profile_id = self.request.query_params.get('profile_id')

        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        
        return queryset
    

class EmployerProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = StaffEmployerProfileSerializers

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id
        queryset = EmployerCompany.objects.filter(user__id=user_id)
        return queryset

    # @swagger_auto_schema(
    #     operation_summary="Возвращает профили работодателей, связанные с текущим пользователем"
    # )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EmployerCompanyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    # @swagger_auto_schema(operation_summary="Получить информацию о работодателя")
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        employer_company = EmployerCompany.objects.filter(user__id=user_id)
        serializer = StaffEmployerCompanySerialzers(
            employer_company, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # @swagger_auto_schema(
    #     operation_summary="Создать новую работодателя",
    #     request_body=StaffEmployerCompanySerialzers,
    # )
    def post(self, request, *args, **kwargs):
        serializer = StaffEmployerCompanySerialzers(data=request.data)

        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    # @swagger_auto_schema(
    #     operation_summary="Обновить информацию  работодателя",
    #     request_body=StaffEmployerUpdateSerialzers,
    # )
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        employer_company = EmployerCompany.objects.get(user=user)
        serializer = StaffEmployerUpdateSerialzers(
            employer_company, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(operation_summary="Получить информацию работодателя")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     operation_summary="Изменить информацию работодателя",
    #     request_body=StaffEmployerUpdateSerialzers,
    # )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

