from applications.accounts.models import User
from rest_framework import serializers
from .models import *
from applications.accounts.serializers import ProfileAllSerializer
from django.contrib.auth import get_user_model
# from schedule.models import Event



User = get_user_model()



class EmployerProfileSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'icon',
            'first_name',
            'last_name',
            'name',
            'description',
        ]

class EmployerCompanySerialzers(serializers.ModelSerializer):
    iin = serializers.CharField(required=False, allow_blank=True)

    icon = serializers.ImageField(required=False, use_url=True,allow_null=True)
  
    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'name',
            'iin',
            'description',
            'icon',
        ]


    def get_url_icon(self, obj):  
        request = self.context.get('request')
        url_icon = obj.icon.url
        return request.build_absolute_uri(url_icon)
    
    
   

class EmployerUpdateSerialzers(serializers.ModelSerializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        iin = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        icon = serializers.ImageField(required=False, use_url=True,allow_null=True)


    
        class Meta:
            model = EmployerCompany
            fields = [
                'id',
                'first_name',
                'last_name',
                'name',
                'iin',
                'description',
                'icon',
            ]
        
        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.name = validated_data.get('name', instance.name)
            instance.iin = validated_data.get('iin', instance.iin)
            instance.description = validated_data.get('description', instance.description)
            instance.icon = validated_data.get('icon', instance.icon)
            instance.save()
            return instance


class CountrySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = [
            'id',
            'name',
        ]

class BranchSerializers(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', required=False, allow_null=True)
    

    class Meta:
        model = Branch
        fields = [
            'id',
            'country',
            'city',
            'name',
            'address',
            'link_address',
            'description',
        ]
  
    def update(self, instance, validated_data):
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.link_address = validated_data.get('link_address', instance.link_address)
        instance.description = validated_data.get('description', instance.description)
    
        instance.save()
        return instance
    

#серилайзер для гет запроса где только название филиала и город
class BranchListSerializers(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name')
    class Meta:
        model = Branch
        fields = [
            'id',
            'country',
            'city',
            'name',
        ]
        

class VacancySerializers(serializers.ModelSerializer):

    class Meta:
        model = Vacancy
        fields = [
            'branch',
            'position', 
            'duty', 
            'experience', 
            'type_of_housing',
            'housing_cost',
            'clothingform', 
            'salary', 
            'vehicle', 
            'insurance', 
            'requirements', 
            'conditions', 
            'employee_count',
            'gender',
            'time_start', 
            'time_end', 
            'holiday_start_date',
            'holiday_end_date',
            'contact_person', 
            'email_info', 
            'phone', 
            'description',
            'language_german',
            'language_english',

        ]
    

    def update(self, instance, validated_data):
        instance.branch = validated_data.get('branch', instance.branch)
        instance.position = validated_data.get('position', instance.position)
        instance.duty = validated_data.get('duty', instance.duty)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.clothingform = validated_data.get('clothingform', instance.clothingform)
        instance.employee_count = validated_data.get('employee_count', instance.employee_count)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.increase_choices = validated_data.get('increase_choices', instance.increase_choices)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class VacancyDetailSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='employer_company.user.id')
    employer_company_icon = serializers.ImageField(source='employer_company.icon')
    employer_company_name = serializers.CharField(source='employer_company.name')
    branch = serializers.CharField(source='branch.name')
    branch_city = serializers.CharField(source='branch.country.name')
    branch_address = serializers.CharField(source='branch.address')
    created_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'user_id', 
            'employer_company_name',
            'employer_company_icon',
            'branch',
            'branch_city',
            'branch_address',
            'position', 
            'duty', 
            'experience', 
            'type_of_housing',
            'housing_cost',
            'clothingform', 
            'salary', 
            'vehicle', 
            'insurance', 
            'requirements', 
            'conditions', 
            'employee_count',
            'employee_count_hired',
            'gender',
            'time_start', 
            'time_end', 
            'contact_person', 
            'email_info', 
            'phone', 
            'description',
            'created_date',
            'language_german',
            'language_english',
            'is_active',
        ]
    
    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")

    def get_employer_company_icon(self, obj):
        request = self.context.get('request')
        url_icon = obj.employer_company.icon.url
        return request.build_absolute_uri(url_icon)


class VacancyListSerializers(serializers.ModelSerializer):
    employer_company_icon = serializers.ImageField(source='employer_company.icon')
    employer_company_name = serializers.CharField(source='employer_company.name')
    branch = serializers.CharField(source='branch.name')
    branch_city = serializers.CharField(source='branch.country.name')
    branch_address = serializers.CharField(source='branch.address')
    created_date = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Vacancy
        fields = [
            'id',
            'employer_company_name',
            'employer_company_icon',
            'branch',
            'branch_city',
            'branch_address',
            'position', 
            'experience', 
            'employee_count',
            'time_start', 
            'time_end', 
            'salary', 
            'created_date',
            ]
    
    
    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")


class InvitationSerializers(serializers.ModelSerializer):
    user_profile = ProfileAllSerializer(source='user', read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    branch = BranchListSerializers(source='vacancy.branch', read_only=True)
    

    
    class Meta:
        model = Invitation
        fields = [
            'id',
            'vacancy',
            'user',
            'user_profile',
            'created_date',
            'branch',
        ]

    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")

    def get_user_profile_icon(self, obj):
        request = self.context.get('request')
        url_icon = obj.user.icon.url
        return request.build_absolute_uri(url_icon)


class InterviewsListSerializers(serializers.ModelSerializer):
    user_profile = ProfileAllSerializer(source='user', read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    interviews_date = serializers.SerializerMethodField(read_only=True)
    vacancy_review = VacancyListSerializers(source='vacancy', read_only=True)

    class Meta:
        model = Interviews
        fields = [
            'id',
            'vacancy_review',
            'user_profile',
            'created_date',
            'interviews_date',
        ]

    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")

    def get_interviews_date(self, obj):
        return obj.interviews_date.strftime("%d.%m.%Y %H:%M")
    

class InterviewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Interviews
        fields = [
            'id',
            'vacancy',
            'user',
            'created_date',
            'interviews_date',
            'is_accepted',
            'is_work',
        ]


class FavoriteListSerializers(serializers.ModelSerializer):
    user_profile = ProfileAllSerializer(source='user', read_only=True)


    class Meta:
        model = Favorite
        fields = [
            'id',
            'user_profile',
            'created_date',
        ]


class FavoriteSerializers(serializers.ModelSerializer):
    
        class Meta:
            model = Favorite
            fields = [
                'id',
                'user',
            ]
    