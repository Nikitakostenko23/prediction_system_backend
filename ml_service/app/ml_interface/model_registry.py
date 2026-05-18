from .estimator import (
    KasBinaryModel, KeeClassicBinaryModel, KeeEversBinaryModel, KeeGlomBinaryModel,
    KasMultilabelModel, KeeClassicMultilabelModel, KeeEversMultilabelModel,
    BaseBinaryModel, BaseMultilabelModel
)


BINARY_MODELS: dict[str, BaseBinaryModel] ={
    "cas": KasBinaryModel(),
    "cee_classic": KeeClassicBinaryModel(),
    "cee_eversional": KeeEversBinaryModel(),
    "cee_preserve_glomus": KeeGlomBinaryModel(),
}

MULTILABEL_MODELS: dict[str, BaseMultilabelModel] ={
    "cas_multi_label": KasMultilabelModel(),
    "cee_classic_multi_label": KeeClassicMultilabelModel(),
    "cee_eversional_multi_label": KeeEversMultilabelModel(),
}


def get_binary_model(slug: str) -> BaseBinaryModel:
    """Поиск бинарной модели по заданному slug"""
    if slug not in BINARY_MODELS:
       raise ValueError(f"Бинарная модель по slug {slug} не найдена")
    return BINARY_MODELS[slug]


def get_multilabel_model(slug: str) -> BaseMultilabelModel:
    """Поиск многометочной модели по заданному slug"""
    if slug not in MULTILABEL_MODELS:
        raise ValueError(f"Многометочная модель по slug {slug} не найдена")
    return MULTILABEL_MODELS[slug]