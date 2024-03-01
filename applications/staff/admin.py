from django.contrib import admin
from .models import *
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'department', 'position', 'birthday')
    list_filter = ('department', 'position', 'is_created', 'is_updated', 'is_deleted')
    search_fields = ('user__email', 'first_name', 'last_name', 'department', 'position')
    readonly_fields = ('is_created', 'is_updated', 'is_deleted')

admin.site.register(Employee, EmployeeAdmin)