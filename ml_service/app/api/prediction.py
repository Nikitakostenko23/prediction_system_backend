import time

from fastapi import APIRouter, Response, status

from app.ml_interface import prediction_service
from app.pydantic_models.binary_classification import BinaryClassificationModel
from app.pydantic_models.multi_label_classification import MultiLabelClassificationModel
from app.pydantic_models.response_models import BinaryPredictionModel, MultiLabelPrediction

router = APIRouter()


@router.post('/predict/binary/')
async def predict_binary(data: BinaryClassificationModel):
    """Прогнозирование - бинарная классификация"""
    return prediction_service.predict_binary(data)


@router.post('/predict/multi_label/')
async def predict_multi_label(data: MultiLabelClassificationModel):
    """Прогнозирование - многоточечная классификация"""
    return prediction_service.predict_multilabel(data)
