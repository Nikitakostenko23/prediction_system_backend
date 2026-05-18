from dataclasses import dataclass


@dataclass
class MedicalCardData:
    """Данные медкарты"""

    id: int
    gender: str
    age: int
    degree_of_stenosis_of_the_internal_carotid_artery: str
    stenosis_degree_of_the_contralateral_internal_carotid_artery: str
    calcinosis: str
    abnormal_tortuosity_internal_carotid_artery: str
    chronic_cerebrovascular_insufficiency: str
    angina_pectoris_fc: str
    chronic_heart_failure: str
    functional_class_nyha: str
    chronic_obstructive_pulmonary_disease: str
    history_of_oncological_cancer: str
    symptoms_of_internal_carotid_artery_stenosis: bool
    has_previous_myocardial_infraction: bool
    has_heart_rhythm_disturbances: bool
    has_diabetes: bool
    occlusion_time: int
