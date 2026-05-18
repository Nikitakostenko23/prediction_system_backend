from app.ml_interface.model_registry import get_binary_model, get_multilabel_model
from app.pydantic_models.binary_classification import BinaryClassificationModel
from app.pydantic_models.multi_label_classification import MultiLabelClassificationModel
from app.pydantic_models.response_models import BinaryPredictionModel, MultiLabelPrediction
from app.ml_interface.convertor import medical_card_to_dataframe


def predict_binary(data: BinaryClassificationModel) -> BinaryPredictionModel:
    """Процесс предсказания для бинарной классификации"""
    model = get_binary_model(data.ml_model_slug)
    df = medical_card_to_dataframe(data.medical_card)
    proba = model.predict_proba(df)
    prob = float(proba[0]) if proba.ndim == 1 else float(proba[0][0])
    prob = round(prob, 2)

    return BinaryPredictionModel(probability=prob)


def predict_multilabel(data: MultiLabelClassificationModel) -> MultiLabelPrediction:
    """Процесс предсказания для многометочной классификации"""
    model = get_multilabel_model(data.ml_model_slug)
    df = medical_card_to_dataframe(data.medical_card)
    proba = model.predict_proba(df)
    proba = proba[0]

    if len(data.complication_group_slugs) != len(proba):
        raise ValueError("Количество осложнений не соответствует размеру выходных данных модели")
    result = {slug: round(float(proba[i]), 2) for i, slug in enumerate(sorted(data.complication_group_slugs))}

    return MultiLabelPrediction(probability_by_group_slug=result)