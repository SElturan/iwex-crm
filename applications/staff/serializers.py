from rest_framework import serializers
from applications.accounts.models import *
from applications.core.models import *
from .models import *
from applications.accounts.serializers import UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Подставьте соответствующий сериализатор для модели User

    class Meta:
        model = Employee
        fields = ['id', 'user', 'first_name', 'last_name', 'middle_name', 'email', 'department', 'position', 'birthday', 'mobile_phone', 'internal_phone', 'is_created', 'is_updated', 'is_deleted']

class StaffVacationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("start_holiday", "end_holiday")

class StaffProfileAllSerializer(serializers.ModelSerializer):
    universities = StaffVacationsSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "profile_photo",
            "first_name",
            "last_name",
            "gender_en",
            "nationality_en",
            "date_of_birth",
            "phone",
            "english",
            "english_level",
            "russian",
            "russian_level",
            "turkish",
            "turkish_level",
            "chinese",
            "chinese_level",
            "universities",
        )

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "profile_photo",
            "first_name",
            "first_name_ru",
            "last_name",
            "last_name_ru",
            "middle_name",
            "middle_name_ru",
            "gender_ru",
            "gender_en",
            "gender_de",
            "nationality_ru",
            "nationality_en",
            "nationality_de",
            "birth_country_ru",
            "birth_country_en",
            "birth_country_de",
            "birth_region_ru",
            "birth_region_en",
            "birth_region_de",
            "date_of_birth",
            "phone",
            "whatsapp_phone_number",
            "english",
            "english_level",
            "russian",
            "russian_level",
            "turkish",
            "turkish_level",
            "chinese",
            "chinese_level",
        )


class StaffVacancyListSerializers(serializers.ModelSerializer):
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


class StaffInterviewsListSerializers(serializers.ModelSerializer):
    user_profile = StaffProfileAllSerializer(source='user', read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    interviews_date = serializers.SerializerMethodField(read_only=True)
    vacancy_review = StaffVacancyListSerializers(source='vacancy', read_only=True)

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

class StaffInterviewsSerializers(serializers.ModelSerializer):

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

class StaffVacationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("start_holiday", "end_holiday")




class StaffFavoriteListSerializer(serializers.ModelSerializer):
    # user_profile = StaffProfileAllSerializer(source="user", read_only=True)

    class Meta:
        model = Favorite
        fields = (
            "id",
            "employer",
            # "user_profile",
            'user',
            "created_date",
        )


class StaffFavoriteSerializers(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = [
            "id",
            "employer",
            "user",
        ]


class StaffOrderStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStudents
        fields = '__all__'

# -------------------------
        

class PositionEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionEmployee
        fields = ['id', 'name']

class EmployerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompany
        fields = ['id', 'name']

class LandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandName
        fields = ['land_name']

class BranchSerializer(serializers.ModelSerializer):
    branch_land_name = LandNameSerializer()
    
    class Meta:
        model = Branch
        fields = [
            'id','branch_land_name',
            'company', 'name', 'address',
            'link_address', 'description',
            ]


class StaffVacanciesSerializer(serializers.ModelSerializer):
    employer_company = EmployerCompanySerializer()
    position = PositionEmployeeSerializer()
    branch = BranchSerializer()

    class Meta:
        model = Vacancy
        fields = [
            'id','employer_company','branch','position',
            'duty','experience','clothingform','employee_count',
            'employee_count_hired','gender','time_start',
            'time_end','salary','description',
            'created_date','updated_date',
            'language_german','language_english','is_active',
        ]


class StaffEmployerProfileSerializers(serializers.ModelSerializer):
    
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

class StaffEmployerCompanySerialzers(serializers.ModelSerializer):
    iin = serializers.CharField(required=False, allow_blank=True)

    icon = serializers.ImageField(required=False, use_url=True,allow_null=True)
  
    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'first_name',
            'last_name',
            'position',
            'contact_info',
            'contact_person',
            'icon',
            'name',
            'iin',
            'payment_info',
            'description',
        ]



    def get_url_icon(self, obj):  
        request = self.context.get('request')
        url_icon = obj.icon.url
        return request.build_absolute_uri(url_icon)
    
    
   

class StaffEmployerUpdateSerialzers(serializers.ModelSerializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        position = serializers.CharField(required=False)
        contact_info = serializers.CharField(required=False, allow_blank=True)
        contact_person = serializers.CharField(required=False, allow_blank=True)
        name = serializers.CharField(required=False)
        iin = serializers.CharField(required=False, allow_blank=True)
        payment_info = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        icon = serializers.ImageField(required=False, use_url=True,allow_null=True)


    
        class Meta:
            model = EmployerCompany
            fields = [
                'id',
                'first_name',
                'last_name',
                'position',
                'contact_info',
                'contact_person',
                'name',
                'iin',
                'payment_info',
                'description',
                'icon',
            ]
        
        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.position = validated_data.get('position', instance.position)
            instance.contact_info = validated_data.get('contact_info', instance.contact_info)
            instance.contact_person = validated_data.get('contact_person', instance.contact_person)
            instance.name = validated_data.get('name', instance.name)
            instance.iin = validated_data.get('iin', instance.iin)
            instance.payment_info = validated_data.get('payment_info', instance.payment_info)
            instance.description = validated_data.get('description', instance.description)
            instance.icon = validated_data.get('icon', instance.icon)
            instance.save()
            return instance
