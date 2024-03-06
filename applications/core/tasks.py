# tasks.py
from applications.staff.models import Employee
from celery import shared_task
from django.core.mail import send_mail
from .models import EmployerCompany




@shared_task
def send_employee_notification(employee_id):
    # Получить объект сотрудника по его идентификатору
    employee = Employee.objects.get(pk=employee_id)

    # Получить объект работодателя
    employer = EmployerCompany.objects.first()  # Предположим, что здесь есть логика выбора работодателя

    # Отправить уведомление работодателю
    print(f"Уведомление отправлено работодателю {employer} о новом сотруднике {employee}")