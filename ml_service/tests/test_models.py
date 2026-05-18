import pandas as pd
import numpy as np
from unittest.mock import Mock
from app.ml_interface.estimator import BaseBinaryModel, BaseMultilabelModel


class DummyBinaryModel(BaseBinaryModel):

    def __init__(self):
        self.preprocessor = Mock()
        self.reductor = Mock()
        self.model = Mock()
        self.model_is_keras = True
        self.reductor_is_transformer = True

    def _apply_reductor(self, X_proc):
        return X_proc


class DummyMultilabelModel(BaseMultilabelModel):
    def __init__(self):
        self.preprocessor = Mock()
        self.reductor = None
        self.model = Mock()
        self.model_is_keras = False


def test_binary_model_predict_proba_keras():
    model = DummyBinaryModel()
    X = pd.DataFrame({'a': [1]})
    model.preprocessor.transform.return_value = np.array([[1,2,3]])
    model.model.predict.return_value = np.array([[0.7]])  # (1,1)
    proba = model.predict_proba(X)
    assert proba.shape == (1,)
    assert proba[0] == 0.7
    print("\nSUCCESS: test_binary_model_predict_proba_keras")


def test_binary_model_predict():
    model = DummyBinaryModel()
    model.predict_proba = Mock(return_value=np.array([0.3]))
    pred = model.predict(pd.DataFrame())
    assert pred[0] == 0
    model.predict_proba = Mock(return_value=np.array([0.9]))
    pred = model.predict(pd.DataFrame())
    assert pred[0] == 1
    print("\nSUCCESS: test_binary_model_predict")


def test_multilabel_model_predict_proba_sklearn():
    model = DummyMultilabelModel()
    X = pd.DataFrame({'a': [1]})
    model.preprocessor.transform.return_value = np.array([[1,2]])
    model.model.predict_proba.return_value = [
        np.array([[0.2, 0.8]]),
        np.array([[0.3, 0.7]]),
        np.array([[0.9, 0.1]]),
    ]
    proba = model.predict_proba(X)
    assert proba.shape == (1,3)
    np.testing.assert_array_almost_equal(proba[0], [0.8, 0.7, 0.1])
    print("\nSUCCESS: test_multilabel_model_predict_proba_sklearn")
