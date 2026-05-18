import datetime

from django.utils import timezone

from cabinet.dataclasses import MedicalCardData
from cabinet.models import MedicalCard


def get_age_from_birth_date(birth_date: datetime.date) -> int:
    """Получить возраст из даты рождения"""
    today = timezone.now().date()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def convert_medical_card_to_medical_card_data(
    medical_card: MedicalCard,
    occlusion_time: int,
) -> MedicalCardData:
    """Сконвертировать медицинскую карту в данные для сервиса машинного обучения"""
    return MedicalCardData(
        id=medical_card.id,
        gender=medical_card.gender,
        age=get_age_from_birth_date(medical_card.birthday),
        degree_of_stenosis_of_the_internal_carotid_artery=(
            medical_card.degree_of_stenosis_of_the_internal_carotid_artery
        ),
        stenosis_degree_of_the_contralateral_internal_carotid_artery=(
            medical_card.stenosis_degree_of_the_contralateral_internal_carotid_artery
        ),
        calcinosis=medical_card.calcinosis,
        abnormal_tortuosity_internal_carotid_artery=medical_card.abnormal_tortuosity_internal_carotid_artery,
        chronic_cerebrovascular_insufficiency=medical_card.chronic_cerebrovascular_insufficiency,
        angina_pectoris_fc=medical_card.angina_pectoris_fc,
        chronic_heart_failure=medical_card.chronic_heart_failure,
        functional_class_nyha=medical_card.functional_class_nyha,
        chronic_obstructive_pulmonary_disease=medical_card.chronic_obstructive_pulmonary_disease,
        history_of_oncological_cancer=medical_card.history_of_oncological_cancer,
        symptoms_of_internal_carotid_artery_stenosis=medical_card.symptoms_of_internal_carotid_artery_stenosis,
        has_previous_myocardial_infraction=medical_card.has_previous_myocardial_infraction,
        has_heart_rhythm_disturbances=medical_card.has_heart_rhythm_disturbances,
        has_diabetes=medical_card.has_diabetes,
        occlusion_time=occlusion_time,
    )
