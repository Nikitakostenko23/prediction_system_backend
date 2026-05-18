from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import joblib
from keras.models import load_model
import warnings

from app.settings import PROJECT_ROOT

warnings.filterwarnings("ignore", category=UserWarning)


class BaseModelPrediction(ABC):
    """Базовый класс для прогнозирования"""

    def __init__(self, preprocessor_path, model_path, reductor_path=None,
                 model_is_keras=True, reductor_is_transformer=True):
        self.preprocessor = joblib.load(preprocessor_path)
        self.model_is_keras = model_is_keras
        self.reductor_is_transformer = reductor_is_transformer

        self.model = load_model(model_path) if self.model_is_keras else joblib.load(model_path)

        self.reductor = joblib.load(reductor_path) if reductor_path is not None else None

    def _apply_reductor(self, X_proc: np.ndarray) -> np.ndarray:
        """Применяет редуктор к предобработанным данным, если он есть."""
        if self.reductor is None:
            return X_proc
        if self.reductor_is_transformer:
            return self.reductor.transform(X_proc)
        else:
            return X_proc[:, self.reductor]

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Возвращает вероятности положительного класса"""
        pass

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Возвращает бинарные метки на основе порогового значения"""
        proba = self.predict_proba(X)
        return (proba > 0.5).astype(int)


class BaseBinaryModel(BaseModelPrediction):
    """Базовый класс для моделей бинарной классификации"""

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Возвращает вероятности положительного класса"""
        X_proc = self.preprocessor.transform(X)
        X_reduct = self._apply_reductor(X_proc)

        if self.model_is_keras:
            proba = self.model.predict(X_reduct)
            if proba.ndim == 2 and proba.shape[1] == 1:
                proba = proba.ravel()
            return proba
        else:
            proba = self.model.predict_proba(X_reduct)
            return proba[:, 1]


class BaseMultilabelModel(BaseModelPrediction):
    """Базовый класс для моделей многометочной классификации"""

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Возвращает вероятности положительного класса"""
        X_proc = self.preprocessor.transform(X)
        X_reduct = self._apply_reductor(X_proc)

        if self.model_is_keras:
            proba = self.model.predict(X_reduct)
            if proba.ndim == 3 and proba.shape[-1] == 2:
                return proba[:, :, 1]
            else:
                return proba
        else:
            proba_list = self.model.predict_proba(X_reduct)
            if isinstance(proba_list, list):
                return np.column_stack([p[:, 1] for p in proba_list])
            else:
                return proba_list


class KasBinaryModel(BaseBinaryModel):
    """Модель для бинарной классификации КАС"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KAS/binary/kas_binary_preprocessor.pkl',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KAS/binary/kas_binary_lda.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KAS/binary/kas_binary_neural_net_lda.keras',
            model_is_keras=True,
            reductor_is_transformer=True,
        )


class KeeClassicBinaryModel(BaseBinaryModel):
    """Модель для бинарной классификации КЭЭ классической"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/binary/kee_classic_binary_preprocessor.pkl',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/binary/kee_classic_binary_lda.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/binary/kee_classic_binary_neural_net_lda.keras',
            model_is_keras=True,
            reductor_is_transformer=True,
        )


class KeeEversBinaryModel(BaseBinaryModel):
    """Модель для бинарной классификации КЭЭ эверсионной"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KEE_evers/binary/kee_evers_binary_preprocessor.pkl',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KEE_evers/binary/kee_evers_binary_pca.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KEE_evers/binary/kee_evers_binary_neural_net_pca.keras',
            model_is_keras=True,
            reductor_is_transformer=True,
        )


class KeeGlomBinaryModel(BaseBinaryModel):
    """Модель для бинарной классификации КЭЭ гломуссохраняющей"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KEE_glom/binary/kee_glom_binary_preprocessor.pkl',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KEE_glom/binary/kee_glom_binary_sbs.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KEE_glom/binary/kee_glom_binary_forest_sbs.pkl',
            model_is_keras=False,
            reductor_is_transformer=False,
        )


class KasMultilabelModel(BaseMultilabelModel):
    """Модель для многометочной классификации КАС"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KAS/multilabel/kas_multilabel_preprocessor.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KAS/multilabel/kas_multilabel_forest_sbs.pkl',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KAS/multilabel/kas_multilabel_sbs.pkl',
            model_is_keras=False,
            reductor_is_transformer=False,
        )


class KeeClassicMultilabelModel(BaseMultilabelModel):
    """Модель для многометочной классификации КЭЭ классической"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/multilabel/kee_classic_multi_preprocessor.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/multilabel/kee_classic_multilabel_neural_net_pca.keras',
            reductor_path=PROJECT_ROOT / 'ml_interface/models/KEE_classic/multilabel/kee_classic_multilabel_pca.pkl',
            model_is_keras=True,
            reductor_is_transformer=True,
        )


class KeeEversMultilabelModel(BaseMultilabelModel):
    """Модель для многометочной классификации КЭЭ эверсионной"""

    def __init__(self):
        super().__init__(
            preprocessor_path=PROJECT_ROOT / 'ml_interface/models/KEE_evers/multilabel/kee_evers_multilabel_preprocessor.pkl',
            model_path=PROJECT_ROOT / 'ml_interface/models/KEE_evers/multilabel/kee_evers_multilabel_neural_net.keras',
            reductor_path=None,
            model_is_keras=True,
            reductor_is_transformer=True,
        )
