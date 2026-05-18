import pandas as pd
from app.pydantic_models.medical_card import (
    MedicalCardModel, Gender, InternalCarotidArteryStenosisDegree,
    ContralateralInternalCarotidArteryStenosisDegree, Calcinosis,
    AbnormalTortuosityInternalCarotidArtery, Degree, HeartFailureStage,
    FunctionalClassNyha, ChronicObstructivePulmonaryDisease, Oncology
)
from app.ml_interface.convertor import medical_card_to_dataframe

def test_medical_card_to_dataframe():
    card = MedicalCardModel(
        id=1,
        gender=Gender.MALE,
        age=65,
        degree_of_stenosis_of_the_internal_carotid_artery=InternalCarotidArteryStenosisDegree.FROM_70_TO_89,
        stenosis_degree_of_the_contralateral_internal_carotid_artery=ContralateralInternalCarotidArteryStenosisDegree.FROM_0_TO_49,
        calcinosis=Calcinosis.UNEXPRESSED,
        abnormal_tortuosity_internal_carotid_artery=AbnormalTortuosityInternalCarotidArtery.YES,
        chronic_cerebrovascular_insufficiency=Degree.DEGREE_2,
        angina_pectoris_fc=Degree.DEGREE_1,
        chronic_heart_failure=HeartFailureStage.STAGE_2_A,
        functional_class_nyha=FunctionalClassNyha.FC_2,
        symptoms_of_internal_carotid_artery_stenosis=True,
        has_previous_myocardial_infraction=False,
        has_heart_rhythm_disturbances=True,
        has_diabetes=False,
        chronic_obstructive_pulmonary_disease=ChronicObstructivePulmonaryDisease.DEGREE_1,
        history_of_oncological_cancer=Oncology.NO,
        occlusion_time=30,
    )
    df = medical_card_to_dataframe(card)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 17)

    assert df.loc[0, 'symptoms_of_internal_carotid_artery_stenosis'] == '1'
    assert df.loc[0, 'pim'] == '0'
    assert df.loc[0, 'heart_rhythm_disturbances'] == '1'
    assert df.loc[0, 'sd'] == '0'

    assert df.loc[0, 'gender'] == 'м'
    assert df.loc[0, 'degree_of_stenosis_of_the_internal_carotid_artery'] == '70-89'
    assert df.loc[0, 'hsn'] == '2 a'
    assert df.loc[0, 'FC_by_NYHA'] == '2'

    expected_cols = [
        'gender', 'age', 'degree_of_stenosis_of_the_internal_carotid_artery',
        'stenosis_degree_of_the_contralateral_internal_carotid_artery', 'calcinosis',
        'pivsa', 'symptoms_of_internal_carotid_artery_stenosis', 'hsmn',
        'angina_pectoris_FC', 'pim', 'heart_rhythm_disturbances', 'hsn',
        'FC_by_NYHA', 'sd', 'hobl', 'history_of_oncological_cancer', 'occlusion_time'
    ]
    assert list(df.columns) == expected_cols
    print("\nSUCCESS: test_medical_card_to_dataframe")