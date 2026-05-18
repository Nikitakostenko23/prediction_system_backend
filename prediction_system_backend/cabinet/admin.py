from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from cabinet.models import (
    PredictionUser,
    MedicalCard,
    Complication,
    ComplicationGroup,
    StentingType,
    PredictionRun,
    Prediction,
)


@admin.register(PredictionUser)
class PredictionUserAdmin(UserAdmin):
    """Админ для модели PredictionUser"""

    model = PredictionUser
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['username', 'first_name', 'last_name', 'gender', 'birthday']
    search_fields = ['username', 'first_name', 'last_name', 'gender']
    list_filter = ['gender']
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    fieldsets = [
        (
            'Сведения о пользователе',
            {
                'fields': [
                    'last_name',
                    'first_name',
                    'middle_name',
                    'gender',
                ],
            },
        ),
        (
            'Система',
            {
                'fields': [
                    'username',
                    'password',
                    'email',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'last_login',
                    'groups',
                ],
            },
        ),
    ]
    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'last_name',
                    'first_name',
                    'middle_name',
                    'gender',
                    'birthday',
                    'start_date',
                    'groups',
                ),
            },
        ),
    )


@admin.register(MedicalCard)
class MedicalCardAdmin(admin.ModelAdmin):
    """Админ для моедли MedicalCard"""

    list_display = ['last_name', 'first_name', 'middle_name', 'gender', 'birthday']
    list_display_links = ['last_name', 'first_name', 'middle_name']
    list_filter = [
        'gender',
        'degree_of_stenosis_of_the_internal_carotid_artery',
        'stenosis_degree_of_the_contralateral_internal_carotid_artery',
        'calcinosis',
        'abnormal_tortuosity_internal_carotid_artery',
        'symptoms_of_internal_carotid_artery_stenosis',
        'chronic_cerebrovascular_insufficiency',
        'angina_pectoris_fc',
        'has_previous_myocardial_infraction',
        'has_heart_rhythm_disturbances',
        'chronic_heart_failure',
        'functional_class_nyha',
        'has_diabetes',
        'chronic_obstructive_pulmonary_disease',
        'history_of_oncological_cancer',
    ]
    raw_id_fields = ['created_by']


@admin.register(Complication)
class ComplicationAdmin(admin.ModelAdmin):
    """Админ для моедли Complication"""

    list_display = ['name']


@admin.register(ComplicationGroup)
class ComplicationGroupAdmin(admin.ModelAdmin):
    """Админ для моедли Complication"""

    list_display = ['name']


@admin.register(StentingType)
class StentingTypeAdmin(admin.ModelAdmin):
    """Админ для моедли StentingType"""

    list_display = ['name']


@admin.register(PredictionRun)
class PredictionRunAdmin(admin.ModelAdmin):
    """Админ для моедли PredictionRun"""

    list_display = [
        'surgeon',
        'anesthesist',
        'medical_card',
        'status',
        'occlusion_time',
        'stenting_type',
        'summary_probability',
    ]
    list_filter = ['surgeon', 'anesthesist', 'status', 'stenting_type']
    raw_id_fields = ['surgeon', 'anesthesist', 'medical_card']


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Админ для моедли Prediction"""

    list_display = [
        'prediction_run',
        'ml_model',
        'stenting_type',
        'probability',
        'complication_group',
    ]
    list_filter = ['ml_model', 'complication_group']
    raw_id_fields = ['prediction_run']
