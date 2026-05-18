from dataclasses import dataclass


@dataclass
class PredictionData:
    """Спрогнозированные сервисом машинного обучения данные"""

    probability: float


@dataclass
class MultiClassPredictionData:
    """Спрогнозированные мультиклассовые данные"""

    probability_by_group_slug: dict[str, float]
