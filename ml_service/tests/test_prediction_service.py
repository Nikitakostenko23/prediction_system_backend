from app.ml_interface.prediction_service import predict_binary, predict_multilabel
from app.pydantic_models.binary_classification import BinaryClassificationModel
from app.pydantic_models.multi_label_classification import MultiLabelClassificationModel
from app.pydantic_models.medical_card import MedicalCardModel, Gender

card = MedicalCardModel(
    id=1,
    gender=Gender.MALE,
    age=65,
    degree_of_stenosis_of_the_internal_carotid_artery="70-89",
    stenosis_degree_of_the_contralateral_internal_carotid_artery="50-69",
    calcinosis="1",
    abnormal_tortuosity_internal_carotid_artery="0",
    chronic_cerebrovascular_insufficiency="2",
    angina_pectoris_fc="1",
    chronic_heart_failure="2 a",
    functional_class_nyha="II ФК",
    chronic_obstructive_pulmonary_disease="1",
    history_of_oncological_cancer="0",
    symptoms_of_internal_carotid_artery_stenosis=True,
    has_previous_myocardial_infraction=False,
    has_heart_rhythm_disturbances=True,
    has_diabetes=True,
    occlusion_time=45
)

def test_prediction_service():
    binary_data_cas = BinaryClassificationModel(
        ml_model_slug="cas",
        medical_card=card
    )

    binary_data_cee_classic = BinaryClassificationModel(
        ml_model_slug="cee_classic",
        medical_card=card
    )

    binary_data_cee_eversional = BinaryClassificationModel(
        ml_model_slug="cee_eversional",
        medical_card=card
    )

    binary_data_cee_preserve_glomus=  BinaryClassificationModel(
        ml_model_slug="cee_preserve_glomus",
        medical_card=card
    )

    result_binary_cas = predict_binary(binary_data_cas)
    print("[Binary] probability:", result_binary_cas.probability)

    result_binary_cee_classic = predict_binary(binary_data_cee_classic)
    print("[Binary] probability:", result_binary_cee_classic.probability)

    result_binary_cee_eversional = predict_binary(binary_data_cee_eversional)
    print("[Binary] probability:", result_binary_cee_eversional.probability)

    result_binary_cee_preserve_glomus = predict_binary(binary_data_cee_preserve_glomus)
    print("[Binary] probability:", result_binary_cee_preserve_glomus.probability)

    multilabel_data_cas_multi_label = MultiLabelClassificationModel(
        ml_model_slug="cas_multi_label",
        medical_card=card,
        complication_group_slugs={"1_degree", "2_degree", "3_degree"}
    )

    multilabel_data_cee_classic_multi_label = MultiLabelClassificationModel(
        ml_model_slug="cee_classic_multi_label",
        medical_card=card,
        complication_group_slugs={"1_degree", "2_degree", "3_degree"}
    )

    multilabel_data_cee_eversional_multi_label = MultiLabelClassificationModel(
        ml_model_slug="cee_eversional_multi_label",
        medical_card=card,
        complication_group_slugs={"1_degree", "2_degree", "3_degree"}
    )

    result_multilabel_cas =  predict_multilabel(multilabel_data_cas_multi_label)
    print("[MultiLabel] probabilities:", result_multilabel_cas.probability_by_group_slug)

    result_multilabel_cee_classic = predict_multilabel(multilabel_data_cee_classic_multi_label)
    print("[MultiLabel] probabilities:", result_multilabel_cee_classic.probability_by_group_slug)

    result_multilabel_cee_eversional = predict_multilabel(multilabel_data_cee_eversional_multi_label)
    print("[MultiLabel] probabilities:", result_multilabel_cee_eversional.probability_by_group_slug)

    print("SUCCESS: test_prediction_service")
