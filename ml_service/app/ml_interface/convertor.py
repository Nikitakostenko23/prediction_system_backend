import pandas as pd
from app.pydantic_models.medical_card import *


def map_gender(value: Gender) -> str:
    """Преобразует пол 'm'/'f' в 'м'/'ж' для модели."""
    return 'м' if value == Gender.MALE else 'ж'


def map_bool_to_str(value: bool) -> str:
    """Преобразует bool в строку '1'/'0' для one-hot кодирования."""
    return '1' if value else '0'


def map_functional_class_nyha(value: FunctionalClassNyha) -> str:
    """Преобразует функциональный класс NYHA из текстового вида в числовую строку."""
    mapping = {
        '0': '0',
        'I ФК': '1',
        'II ФК': '2',
        'III ФК': '3',
        'IV ФК': '4',
    }
    return mapping[value.value]


def map_oncology(value: Oncology) -> str:
    """Преобразует историю онкозаболеваний в числовую строку для модели."""
    mapping = {
        '0': '0',
        'one_time': '1',
        'repetitive': '2',
    }
    return mapping[value.value]


def medical_card_to_dataframe(card: MedicalCardModel) -> pd.DataFrame:
    """Преобразование Pydantic-модели в один ряд DataFrame с колонками в порядке, ожидаемом моделью."""
    data = {
        'gender': map_gender(card.gender),
        'age': card.age,
        'degree_of_stenosis_of_the_internal_carotid_artery':
            card.degree_of_stenosis_of_the_internal_carotid_artery.value,
        'stenosis_degree_of_the_contralateral_internal_carotid_artery':
            card.stenosis_degree_of_the_contralateral_internal_carotid_artery.value,
        'calcinosis': card.calcinosis.value,
        'pivsa': card.abnormal_tortuosity_internal_carotid_artery.value,
        'symptoms_of_internal_carotid_artery_stenosis':
            map_bool_to_str(card.symptoms_of_internal_carotid_artery_stenosis),
        'hsmn': card.chronic_cerebrovascular_insufficiency.value,
        'angina_pectoris_FC': card.angina_pectoris_fc.value,
        'pim': map_bool_to_str(card.has_previous_myocardial_infraction),
        'heart_rhythm_disturbances': map_bool_to_str(card.has_heart_rhythm_disturbances),
        'hsn': card.chronic_heart_failure.value,
        'FC_by_NYHA': map_functional_class_nyha(card.functional_class_nyha),
        'sd': map_bool_to_str(card.has_diabetes),
        'hobl': card.chronic_obstructive_pulmonary_disease.value,
        'history_of_oncological_cancer': map_oncology(card.history_of_oncological_cancer),
        'occlusion_time': card.occlusion_time,
    }

    expected_columns = [
        'gender', 'age', 'degree_of_stenosis_of_the_internal_carotid_artery',
        'stenosis_degree_of_the_contralateral_internal_carotid_artery', 'calcinosis',
        'pivsa', 'symptoms_of_internal_carotid_artery_stenosis', 'hsmn',
        'angina_pectoris_FC', 'pim', 'heart_rhythm_disturbances', 'hsn',
        'FC_by_NYHA', 'sd', 'hobl', 'history_of_oncological_cancer', 'occlusion_time'
    ]

    df = pd.DataFrame([data])[expected_columns]
    return df