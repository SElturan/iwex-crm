import django_filters
from django.contrib.auth import get_user_model
from .models import Profile
from applications.core.models import Vacancy
from django.db.models import Q



class ProfileFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(choices=Profile.GENDER_CHOICES_RU, field_name='gender_ru')
    
    german = django_filters.ChoiceFilter(choices=Profile.LANGUAGE_LEVEL_CHOICES, field_name='german_level')
    german_level = django_filters.ChoiceFilter(choices=Profile.LEVEL_CHOICES, field_name='german')

    english = django_filters.ChoiceFilter(choices=Profile.LANGUAGE_LEVEL_CHOICES, field_name='english')
    english_level = django_filters.ChoiceFilter(choices=Profile.LEVEL_CHOICES, field_name='english_level')
    
    turkish = django_filters.ChoiceFilter(choices=Profile.LANGUAGE_LEVEL_CHOICES, field_name='turkish')
    turkish_level = django_filters.ChoiceFilter(choices=Profile.LEVEL_CHOICES, field_name='turkish_level')
    
    russian = django_filters.ChoiceFilter(choices=Profile.LANGUAGE_LEVEL_CHOICES, field_name='russian')
    russian_level = django_filters.ChoiceFilter(choices=Profile.LEVEL_CHOICES, field_name='russian_level')
    
    chinese = django_filters.ChoiceFilter(choices=Profile.LANGUAGE_LEVEL_CHOICES, field_name='chinese')
    chinese_level = django_filters.ChoiceFilter(choices=Profile.LEVEL_CHOICES, field_name='chinese_level')

    class Meta:
        model = Profile
        fields = [
            'gender', 
            'german', 'german_level',
            'english', 'english_level', 
            'russian', 'russian_level', 
            'turkish', 'turkish_level', 
            'chinese', 'chinese_level',
            ]
