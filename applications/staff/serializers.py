from rest_framework import serializers
from ..accounts.models import Profile




class StaffProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'id', 
            'profile_photo',
            'first_name', 
            'first_name_ru', 
            'last_name', 
            'last_name_ru',
            'middle_name', 
            'middle_name_ru',
            'gender_ru', 
            'gender_en', 
            'gender_de',
            'nationality_ru', 
            'nationality_en', 
            'nationality_de', 
            'birth_country_ru', 
            'birth_country_en', 
            'birth_country_de',
            'birth_region_ru', 
            'birth_region_en', 
            'birth_region_de',
            'date_of_birth', 
            'phone', 
            'whatsapp_phone_number',
            'english', 'english_level', 
            'russian', 'russian_level', 
            'turkish', 'turkish_level', 
            'chinese', 'chinese_level',
            
        )
