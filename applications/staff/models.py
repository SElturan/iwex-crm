from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    first_name = models.CharField(_('Имя'), max_length=50, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=50, blank=True)
    middle_name = models.CharField(_('Отчество'), max_length=50, blank=True)
    email = models.EmailField(_('Контактный Email'), blank=True)
    department = models.CharField(_('Отдел'), max_length=255, blank=True)
    position = models.CharField(_('Должность'), max_length=255, blank=True)
    birthday = models.DateField(_('Дата рождения'), blank=True, null=True)
    mobile_phone = models.CharField(_('Мобильный телефон'), max_length=20, blank=True)
    internal_phone = models.CharField(_('Внутренний телефон'), max_length=20, blank=True)
    is_created = models.BooleanField(_('Запись создана'), default=True)
    is_updated = models.BooleanField(_('Запись обновлена'), default=False)
    is_deleted = models.BooleanField(_('Запись удалена'), default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
