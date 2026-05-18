from pydantic import BaseModel, Field


class BinaryPredictionModel(BaseModel):
    """Ответ эндпоинта бинарной классификации"""

    probability: float = Field(description='Спрогнозированный результат')


class MultiLabelPrediction(BaseModel):
    """Ответ эндпоинта многоточечной классфикации"""

    probability_by_group_slug: dict[str, float] = Field(description='Вероятность осложнений по группе')
