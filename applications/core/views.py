from datetime import date, datetime, timedelta

from applications.accounts.models import User
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from .tasks import send_notification

# from schedule.models import Event
from .models import *
from .serializers import *
from .permissions import IsEmployerPermission
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .permissions import IsEmployerPermission

class EmployerProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = EmployerProfileSerializers

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
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(operation_summary="Получить информацию о работодателя")
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        employer_company = EmployerCompany.objects.filter(user__id=user_id)
        serializer = EmployerCompanySerialzers(
            employer_company, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # @swagger_auto_schema(
    #     operation_summary="Создать новую работодателя",
    #     request_body=EmployerCompanySerialzers,
    # )
    def post(self, request, *args, **kwargs):
        serializer = EmployerCompanySerialzers(data=request.data)

        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="Обновить информацию  работодателя",
    #     request_body=EmployerUpdateSerialzers,
    # )
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        employer_company = EmployerCompany.objects.get(user=user)
        serializer = EmployerUpdateSerialzers(
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
    #     request_body=EmployerUpdateSerialzers,
    # )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CountryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    # @swagger_auto_schema(operation_summary="Получить список земли")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BranchAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="создать филиал", request_body=BranchSerializers
    # )
    def post(self, request, *args, **kwargs):
        serializer = BranchSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            employer_company = get_object_or_404(EmployerCompany, user__id=user_id)

         
            serializer.save(company=employer_company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="Обновить информацию о филиале",
    #     request_body=BranchSerializers,
    # )
    def patch(self, request, *args, **kwargs):
        branch_id = self.kwargs["pk"]
        branch = Branch.objects.get(id=branch_id)
        user = request.user
        serializer = BranchSerializers(branch, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchListAPIView(ListAPIView):
    serializer_class = BranchListSerializers
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Branch.objects.filter(company__user__id=user_id).select_related(
            "country", "company"
        )
        return queryset

    # @swagger_auto_schema(operation_summary="Получить список филиалов пользователя")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BranchDetailListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = BranchSerializers

    def get_queryset(self):
        branch_id = self.request.query_params.get("branch_id", None)
        if not branch_id:
            return Branch.objects.none()

        # Используйте filter(id=branch_id) вместо filter(branch=branch)
        branch = get_object_or_404(Branch, id=branch_id)
        queryset = Branch.objects.filter(id=branch.id).select_related(
            "country", "company"
        )
        return queryset

    # @swagger_auto_schema(operation_summary="Получить информацию о конкретном филиале")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HousingAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    def post(self, request, *args, **kwargs):
        serializer = HousingSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            try:

                employer_company = EmployerCompany.objects.get(id=user_id)
            except EmployerCompany.DoesNotExist:
                return Response({'error': 'Add a company to add applications'}, status=status.HTTP_400_BAD_REQUEST)
            housing = serializer.save(employer=employer_company)

            files_data = request.FILES.getlist("files")  # Получаем список видео
            for file_data in files_data:
                FilesHousing.objects.create(housing=housing, files=file_data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HousingListAPIView(ListAPIView):
    serializer_class = HousingListSerializers
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Housing.objects.filter(employer__user__id=user_id).select_related('employer',)
        return queryset

class VacancyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="Создать новую вакансию и связать ее с компанией и филиалом",
    #     request_body=VacancySerializers,
    # )
    def post(self, request, *args, **kwargs):
        serializer = VacancySerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            branch = request.data.get("branch")

            user = EmployerCompany.objects.get(user__id=user_id)

            # выводим только его филлиалы и проверяем есть ли у него такой филлиал
            branch = Branch.objects.filter(company=user).filter(id=branch).first()

            if user is None:
                return Response(
                    {"error": "Add a company to add applications"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if branch is None:
                return Response(
                    {"error": "Branch is missing."}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(
                employer_company=user,
                branch=branch,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacancyUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="Обновить информацию о вакансии",
    #     request_body=VacancySerializers,
    # )
    def patch(self, request, *args, **kwargs):
        vacancy_id = kwargs["pk"]
        vacancy = Vacancy.objects.get(id=vacancy_id)

        serializer = VacancySerializers(vacancy, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacancyListAPIView(ListAPIView):
    serializer_class = VacancyListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "branch__name",
    ]

    def get_queryset(self):
        queryset = Vacancy.objects.all().select_related(
            "employer_company",
            "branch",
        )
        return queryset

    # @swagger_auto_schema(
    #     operation_summary="Получить список вакансий с возможностью поиска по названию филиала"
    # )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VacancyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # @swagger_auto_schema(operation_summary="Получить детали конкретной вакансии")
    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs["pk"]
        vacancy = (
            Vacancy.objects.filter(id=vacancy_id)
            .select_related(
                "employer_company",
                "branch",
            )
            .first()
        )

        if vacancy is None:
            return Response(
                {"error": "Vacancy is missing."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VacancyDetailSerializers(vacancy, context={"request": request})
        return Response(serializer.data)


class EmployerVacancyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = VacancyListSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(EmployerCompany, user__id=user_id)
        queryset = Vacancy.objects.filter(employer_company=user).select_related(
            "employer_company",
            "branch",
        )
        return queryset

    # @swagger_auto_schema(
    #     operation_summary="Получить список вакансий для текущего работодателя"
    # )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InvitationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]

    # @swagger_auto_schema(
    #     operation_summary="Получить список приглашений для текущего работодателя"
    # )
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        invitation = Invitation.objects.filter(
            employer__user__id=user_id
        ).select_related(
            "employer",
            "vacancy",
            "user",
        )
        serializer = InvitationSerializers(
            invitation, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # @swagger_auto_schema(
    #     operation_summary="Создать новое приглашение",
    #     request_body=InvitationSerializers,
    # )
    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get("vacancy")
            user = request.data.get("user")
            invitation = (
                Invitation.objects.filter(employer__user__id=user_id)
                .filter(vacancy=vacancy)
                .filter(user=user)
                .first()
            )
            if invitation is not None:
                return Response(
                    {"error": "You have already invited this applicant"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = EmployerCompany.objects.get(user__id=user_id)
            vacancy = (
                Vacancy.objects.filter(employer_company=user).filter(id=vacancy).first()
            )
            if vacancy is None:
                return Response(
                    {"error": "Vacancy is missing."}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(employer=user, vacancy=vacancy)
     
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterviewsModelViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = InterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "vacancy",
    ]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Interviews.objects.filter(employer__user__id=user_id).select_related(
            "vacancy",
            "user",
        )
        return queryset

    # @swagger_auto_schema(
    #     operation_summary="Получить список собеседование для текущего работодателя"
    # )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class InterviewsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = InterviewsSerializers

    # @swagger_auto_schema(
    #     operation_summary="Создать новое собеседования",
    #     request_body=InterviewsSerializers,
    # )
    def post(self, request, *args, **kwargs):
        serializer = InterviewsSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get("vacancy")
            user = request.data.get("user")
            invitation = (
                Interviews.objects.filter(employer__user__id=user_id)
                .filter(vacancy=vacancy)
                .filter(user=user)
                .first()
            )
            if invitation is not None:
                return Response(
                    {"error": "You have already invited this applicant"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = EmployerCompany.objects.get(user__id=user_id)
            vacancy = (
                Vacancy.objects.filter(employer_company=user).filter(id=vacancy).first()
            )
            if vacancy is None:
                return Response(
                    {"error": "Vacancy is missing."}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(employer=user, vacancy=vacancy)
            channel_layer = get_channel_layer()
            
            async_to_sync(channel_layer.group_send)(
                f'notification_{user_id}', {
                    'type': 'interviews_message',
                    'message': 'You have a new invitation',
                    'user_id': "test"
                }
            )


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = FavoriteListSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Favorite.objects.filter(employer__user__id=user_id).select_related(
            "user",
        )
        return queryset

    # @swagger_auto_schema(
    #     operation_summary="Получить список избранных пользователей для текущего работодателя"
    # )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FavoriteAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermission]
    serializer_class = FavoriteSerializers

    # @swagger_auto_schema(operation_summary="Добавить пользователя в избранное")
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        user = request.data.get("user")

        # Проверяем, не добавлен ли уже этот пользователь в избранное
        if Favorite.objects.filter(employer__user__id=user_id, user=user).exists():
            return Response(
                {"error": "You have already added this user to favorites"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Получаем работодателя и сохраняем в избранное
        employer = EmployerCompany.objects.get(user__id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=employer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderStudentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderStudentsSerializer
    permission_classes = [IsAuthenticated, IsEmployerPermission]
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


class NotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        message = request.data.get("message")
        if email and message:
            send_notification.delay(email, message)  # Запуск задачи Celery
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Email and message are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SendNotificationView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        result = send_notification.delay(user_id, message)
        print(result.get())  # Получаем результат задачи и выводим на консоль
        return Response({'status': 'Notification sent'}, status=status.HTTP_200_OK)