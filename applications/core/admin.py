from django.contrib import admin, messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *
from applications.staff.models import Notification

class EmployerCompanyAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','name','iin','description','icon',]
    search_fields = ['user','first_name','last_name','name','iin','description','icon',]

    ordering = ('id',)
    class Meta:
        model = EmployerCompany

class BranchAdmin(admin.ModelAdmin):
    list_display = ['id','city','company','name','address','link_address','description',]
    search_fields = ['city','company','name','address','link_address','description',]

    ordering = ('id',)
    class Meta:
        model = Branch



class FilesInline(admin.StackedInline):
    model = FilesHousing
    extra = 1

class HousingAdmin(admin.ModelAdmin):
    list_display = ['id','housing_type',]

    inlines = [FilesInline]

class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'id','employer_company','branch','position','salary',
        'time_start',
        ]
    search_fields = [
        'employer_company','branch','position',
        ]

    ordering = ('id',)

    class Meta:
        model = Vacancy


class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id','employer','vacancy','user', 'is_rejected', 'is_accepted']
    ordering = ('id',)
    class Meta:
        model = Invitation

class OrderStudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'employer_sender', 'branch', 'language_german_level', 'language_english_level', 'number_of_students', 'recipient_employee', 'created_date')
    list_filter = ('branch', 'language_german_level', 'language_english_level', 'created_date')
    search_fields = ('employer_sender__name', 'branch__name', 'recipient_employee__first_name', 'recipient_employee__last_name')
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date',)

admin.site.register(OrderStudents, OrderStudentsAdmin)


admin.site.register(Favorite)
admin.site.register(Country)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(EmployerCompany, EmployerCompanyAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Interviews)
admin.site.register(Housing, HousingAdmin)
