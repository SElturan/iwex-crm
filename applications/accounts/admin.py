import os
import csv
import xlsxwriter
from django.contrib import admin, messages
from .models import *
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch 



class ExportAdminMixin:
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        fields = [field for field in self.model._meta.fields if not field.many_to_many and not field.one_to_many]
        writer.writerow([field.name for field in fields])
        for obj in queryset:
            writer.writerow([getattr(obj, field.name) for field in fields])
        return response

    export_csv.short_description = "Export to CSV"

    def export_xlsx(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()
        fields = [field for field in self.model._meta.fields if not field.many_to_many and not field.one_to_many]
        for col_num, field in enumerate(fields):
            worksheet.write(0, col_num, field.name)
        for row_num, obj in enumerate(queryset, start=1):
            for col_num, field in enumerate(fields):
                worksheet.write(row_num, col_num, str(getattr(obj, field.name)))
        workbook.close()
        return response

    export_xlsx.short_description = "Export to XLSX"


@admin.register(User)
class UserAdmin(ExportAdminMixin, BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'verification_code',
                           'is_verified_email', 'password', 'is_delete',)}),
        (_('Permissions'), {'fields': ('role','is_staff', 'is_active', 
                                       'is_superuser','user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1','password2', 
                       'is_delete', 'is_active', 'is_superuser', ),
        }),
    )
    list_display = ['id','email','verification_code', 'phone',  
                    'is_staff', 'is_delete', 'is_active','role', 'is_superuser', ]
    search_fields = ['email', 'phone',  ]
    list_editable = ['is_staff', 'is_delete', 'is_active','role',  'is_superuser',]
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')

    actions = ['export_csv', 'export_xlsx', 'export_pdf']

    class Meta:
        model = User

font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesnewromanpsmt.ttf')
class UniversityAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ('id', 'user', 'name_ru', 'degree_type_ru', 'faculty_ru', 'kurs_year')
    search_fields = ['user__email', 'name_ru']

    fieldsets = (
        (None, {
            'fields': ('user', 'name_de','name_en','name_ru', 'degree_type_de',
                       'degree_type_en','degree_type_ru','faculty_de','faculty_en','faculty_ru',
                       'address_de','address_en','address_ru','phone_number_university_ru',
                       'email_university','website_university','start_date','end_date',
                       'total_years','kurs_year','start_holiday','end_holiday')
        }),
    )
    actions = ['export_csv', 'export_xlsx','export_pdf']

    
    
    def export_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="universities.pdf"'
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesnewromanpsmt.ttf')
        pdfmetrics.registerFont(TTFont('Times-Roman', font_path))
        pdf = canvas.Canvas(response)
        pdf.setFont("Times-Roman", 12)
        y_position = 800
        if queryset.exists():
            for obj in queryset:
                y_position -= 20
                pdf.drawString(100, y_position, f'Name RU: {obj.name_en}')
                pdf.drawString(100, y_position - 20, f'Degree Type RU: {obj.degree_type_ru}')
                pdf.drawString(100, y_position - 40, f'Faculty RU: {obj.faculty_ru}')
                pdf.drawString(100, y_position - 60, f'Kurs Year: {obj.kurs_year}')
        else:
            pdf.drawString(100, y_position, "No data available")
        pdf.showPage()
        pdf.save()
        return response
   
    export_pdf.short_description = "Export to PDF"

admin.site.register(University, UniversityAdmin)

class UniversityInline(admin.StackedInline):  
    model = University
    extra = 1


class PassportAndTermInline(admin.StackedInline):  
    model = PassportAndTerm
    extra = 1

class PassportAndTermAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ('user', 'number_id_passport', 'inn', 
                    'passport_number', 'passport_date_of_issue', 
                    'passport_end_time', 'pnr_code', 'term_date_time')
    search_fields = ['user']

    fieldsets = (
        (None, {
            'fields': ('user', 'number_id_passport', 'inn', 
                       'passport_number', 'passport_date_of_issue', 
                       'passport_end_time', 'pnr_code','pdf_file', 
                       'term_date_time')
        }),
    )
    actions = ['export_csv', 'export_xlsx']
admin.site.register(PassportAndTerm, PassportAndTermAdmin)

class PaymentAdmin(admin.ModelAdmin, ExportAdminMixin):
    list_display = ('id', 'user', 'total_amount', 'payment_date',
                    'debt','fully_paid', 'payment_accepted')
    list_filter = ('payment_accepted',)
    search_fields = ('user__email',)
    actions = ['export_csv', 'export_xlsx']
    def save_model(self, request, obj, form, change):
        try:
            if not obj.total_amount:
                raise ValidationError({'__all__': [_('Общая сумма должна быть заполнена')]})
            obj.initial_fee = obj.initial_fee or 0
            obj.average_fee = obj.average_fee or 0
            obj.final_fee = obj.final_fee or 0
            paid_amount = obj.initial_fee + obj.average_fee + obj.final_fee
            if paid_amount > 0:
                obj.payment_accepted = True
                obj.debt = max(0, obj.total_amount - paid_amount)
                obj.fully_paid = 'ДА' if paid_amount == obj.total_amount else 'НЕТ'
            else:
                obj.payment_accepted = False
                obj.debt = obj.total_amount
                obj.fully_paid = 'НЕТ'

            super().save_model(request, obj, form, change)
            messages.success(request, _('Оплата успешно изменена'))
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                messages.error(request, f'{field}: {", ".join(errors)}')

admin.site.register(Payment, PaymentAdmin)

class Payment(admin.StackedInline): 
    model = Payment
    extra = 1


class Deal(admin.StackedInline):
    model = Deal
    extra = 1

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportAdminMixin):

    list_display = (
        'id', 'user', 'first_name', 'last_name', 'nationality_ru',
        'german', 'english', 'russian',
    )

    search_fields = ('user', 'nationality_ru', 'gender_ru', 
                     'english', 'russian', 'german',)
    list_filter = ('gender_ru', 'nationality_ru', 'english', 
                   'russian', 'german',)
    fieldsets = (
        (None, {'fields': (
            'user','first_name_de', 'first_name', 'first_name_ru', 
            'last_name_de','last_name', 'last_name_ru',
            'middle_name_de','middle_name', 'middle_name_ru', 
            'profile_photo',
            'gender_de','gender_en', 'gender_ru', 
            'nationality_de','nationality_en','nationality_ru',  
            'birth_country_de','birth_country_en','birth_country_ru',  
            'birth_region_de','birth_region_en','birth_region_ru',  
            'date_of_birth', 'phone', 'whatsapp_phone_number',
            'german', 'english', 'russian',
        )}),
    )

    def download_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="profiles.pdf"'

            # Создание PDF
        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)

        y_position = 800  # Начальная позиция для текста в PDF

            # Добавление информации о каждом профиле в PDF
        for profile in queryset:
            p.drawString(100, y_position, f"First Name (RU): {profile.first_name_ru}")
            p.drawString(100, y_position - 20, f"First Name (EN): {profile.first_name}")
            p.drawString(100, y_position - 40, f"First Name (DE): {profile.first_name_de}")
            p.drawString(100, y_position - 60, f"Last Name (RU): {profile.last_name_ru}")
                
                # Проверка наличия фото профиля и вставка изображения, если оно есть
            if profile.profile_photo:
                image_path = profile.profile_photo.path  # Получение пути к изображению
                p.drawImage(image_path, 350, y_position - 200, width=3*inch, height=3*inch)
                
            y_position -= 180  # Сдвиг для следующего профиля

        p.showPage()
        p.save()
            
        return response

    download_pdf.short_description = "Download PDF"  # Название вашего действия в административном интерфейсе
    # Добавление действия в административный интерфейс
    actions = ["download_pdf", 'export_csv', 'export_xlsx']

    inlines = [
        UniversityInline, PassportAndTermInline, 
        Payment, Deal,]  # Добавляем в профиль инлайн университета
    



# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'study_certificate', 'study_certificate_embassy', 'study_certificate_translate_embassy',
#                     'photo_for_schengen', 'zagranpassport_copy', 'passport_copy', 'fluorography_express',
#                     'fluorography', 'immatrikulation', 'transcript', 'transcript_translate', 'bank_statement',
#                     'conduct_certificate', 'mentaldispanser_certificate', 'drugdispanser_certificate',
#                     'parental_permission', 'bank_details', 'visa_file')
#     search_fields = ('user',)
    
# admin.site.register(Documents, DocumentAdmin)


# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'value_rating', 'rating_date', 'employer',)
#     search_fields = ('user__email', 'value_rating', 'employer',)



# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('employer', 'user', 'text', 'creation_date')
#     search_fields = ('user__email', 'text')




# @admin.register(WorkExperience)
# class WorkExperienceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'type_company', 'company', 'position', 'start_date', 'country',)
#     search_fields = ('user__email', 'company', 'position', 'country',)
#     list_filter = ('type_company', 'position', 'country',)


#     fieldsets = (
#         (None, {'fields': ('user', )}),
#         ('Details', {'fields': ('company', 'type_company', 'position',)}),
#         ('Worktime', {'fields': ('start_date', 'end_date',)}),
#         ('Important dates', {'fields': ('responsibilities', 'country',)}),
#     )




# @admin.register(WorkSchedule)
# class WorkScheduleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user',)
#     search_fields = ('user__email',)
#     fields = (
#         'user', 'monday', 'tuesday', 
#         'wednesday', 'thursday', 'friday', 
#         'saturday', 'sunday', 
#         'custom', 
#         'custom_start_time', 'custom_end_time',
#         )