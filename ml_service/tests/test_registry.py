import pytest
from app.ml_interface.model_registry import (BINARY_MODELS, MULTILABEL_MODELS,
                                             get_binary_model, get_multilabel_model)

def test_registry_contains_expected_keys():
    expected_binary = {"cas", "cee_classic", "cee_eversional", "cee_preserve_glomus"}
    assert set(BINARY_MODELS.keys()) == expected_binary
    expected_multi = {"cas_multi_label", "cee_classic_multi_label", "cee_eversional_multi_label"}
    assert set(MULTILABEL_MODELS.keys()) == expected_multi
    print("\nSUCCESS: test_registry_contains_expected_keys")

def test_get_binary_model_valid():
    model = get_binary_model("cas")
    from app.ml_interface.estimator import KasBinaryModel
    assert isinstance(model, KasBinaryModel)
    print("\nSUCCESS: test_get_binary_model_valid")

def test_get_binary_model_invalid():
    with pytest.raises(ValueError, match="Бинарная модель по slug unknown не найдена"):
        get_binary_model("unknown")
    print("\nSUCCESS: test_get_binary_model_invalid")

def test_get_multilabel_model_valid():
    model = get_multilabel_model("cas_multi_label")
    from app.ml_interface.estimator import KasMultilabelModel
    assert isinstance(model, KasMultilabelModel)
    print("\nSUCCESS: test_get_multilabel_model_valid")