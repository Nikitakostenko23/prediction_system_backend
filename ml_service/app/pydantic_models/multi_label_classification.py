from pydantic import BaseModel, Field

from app.pydantic_models.medical_card import MedicalCardModel


class MultiLabelClassificationModel(BaseModel):
    """Входные данные для многоточечной классфиикации"""

    ml_model_slug: str = Field(description="Слаг модели машинного обучения", min_length=1)
    medical_card: MedicalCardModel = Field(description='Данные из медицинской карты')
    complication_group_slugs: frozenset[str] = Field(description='Слаги групп осложнений')
