# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification(email, message):
    """
    Функция для отправки уведомления на email.
    """
    subject = 'Уведомление'
    message = f'Уведомление: {message}'
    from_email = 'your_email@example.com'  # Укажите ваш адрес электронной почты
    to_email = [email]
    send_mail(subject, message, from_email, to_email)
