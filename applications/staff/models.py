# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
# from accounts.models import Vacancy

# User = get_user_model()

# class Task(models.Model):
#     user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
#     vacancy = models.ForeignKey(Vacancy, related_name='tasks', on_delete=models.CASCADE, verbose_name=_('Вакансия'))
#     description = models.CharField(_('Описание задачи'), max_length=255)
#     deadline = models.DateField(_('Срок выполнения'))
#     completed = models.BooleanField(_('Выполнено'), default=False)

#     def __str__(self):
#         return self.description
