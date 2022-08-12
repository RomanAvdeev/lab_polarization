from typing import List

from pydantic import BaseModel, Field

from schemas.document import Topic


class DocumentPolarization(BaseModel):
    document_id: int = Field(..., title="Уникальный ID документа")
    probabilities: List[float] = Field(..., title="Оценки вероятности для каждого из полюсов")
    neutral: bool = Field(..., title="Является ли документ нейтральным (не поляризованным)")
    neutral_prob: float = Field(
        ..., title="Вероятность что документ является нейтральным (не поляризованным)"
    )
    irrelevant: bool = Field(
        ...,
        title="Является ли документ нерелевантным (не имеющим отношения к общей тематике входных сообщений)",
    )
    irrelevant_prob: float = Field(
        ...,
        title="Вероятность что документ является нерелевантным (не имеющим отношения к общей тематике входных сообщений)",
    )


class TopicPolarization(BaseModel):
    documents_polarization: List[DocumentPolarization] = Field(
        ..., title="Список документов с информацией о поляризации для каждого из них"
    )
    num_poles: int = Field(..., title="Количество полюсов мнений")
    poles_names: List[str] = Field(
        ..., title="Короткое автоматически выбираемое название для каждого из полюсов мнений"
    )
    polarization_ner: List[str] = Field(
        ..., title="Cписок сущностей, относительно которых происходит поляризация мнений"
    )
    entities_relations_to_poles: List[List[float]] = Field(
        ..., title="Матрица отношений сущностей к полюсам"
    )
    topic: Topic = Field(..., title="Тема кластера")
    tension: float = Field(..., title="Оценка напряжённости поляризации")
    significance: float = Field(..., title="Оценка значимости поляризации ")


class Metrics(BaseModel):
    precision: float
    recall: float
    f1_score: float
    