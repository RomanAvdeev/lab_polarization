from typing import List, Optional, Tuple

from pydantic import BaseModel, Field
from pydantic.types import conlist


class Sentences(BaseModel):
    """
    Разделение документа на предложения. В исходных данных находится в поле ner_result
    """

    sentences: List[str] = Field(..., title="Список предложений в документе")
    sentences_offsets: List[List[int]] = Field(
        ..., title="Список координат начала и конца предложений в оригинальном тексте"
    )


class NelFeatures(BaseModel):
    """
    Named entity linking для документа. Схема аналогична полю nel_result в наборе данных
    """

    entities: List[str] = Field(..., title="Список именованных сущностей")
    entities_offset: List[List[int]] = Field(
        ..., title="Список координат начала и конца именованной сущности в оригинальном тексте"
    )
    entities_tag: List[str] = Field(
        ..., title="Список тегов для именованных сущностей из поля entities"
    )
    linked_entities: List[List[str]] = Field(
        ...,
        title="Список именнованных сущностей из WikiData, связанных в найденной в тексте сущностью",
    )
    wiki_id: List[conlist(str, min_items=1, max_items=5)] = Field(
        ...,
        title="Список ID именнованных сущностей из WikiData, связанных в найденной в тексте сущностью",
    )
    other: List[List[List[float]]] = Field(
        ...,
        title="Для каждой wiki-сущности три числа: 1. насколько сущность из текста матчится с названием wiki-сущности, 2. Количество ребер у wiki-сущности в графе, 3. Сontext confindence - насколько описание сущности в викидате подходит под контекст",
    )


class WordFeatures(BaseModel):
    """
    Признаки слова в н-грамме
    """

    case: Optional[str]
    degree: Optional[str]
    animacy: Optional[str]
    gender: Optional[str]
    number: Optional[str]


class NgramWord(BaseModel):
    form: str = Field(..., title="Слово в н-грамме")
    upos: str
    xpos: Optional[str]
    feats: WordFeatures
    head: int = Field(..., title="Индекс главного слова")
    deprel: str = Field(..., title="Тип зависимости между словами")
    start_idx: int = Field(..., title="Индекс начала н-граммы в тексте")
    end_idx: int = Field(..., title="Индекс конца н-граммы в тексте")


class Ngram(BaseModel):
    name: str = Field(..., title="Текст н-граммы")
    ngram_words: List[NgramWord] = Field(
        ..., title="Список слов в н-грамме с дополнительными признаками"
    )


# class NgramFeatures(BaseModel):
#     """
#     Ngrams для документа (!Состав и типы полей уточнится после получения данных!)
#     """

#     entities: List[str] = Field(..., title="Список ngrams")
#     offsets: List[Tuple[int, int]] = Field(..., title="Список координат начала и конца ngrams")


class TopicInfo(BaseModel):
    id: str = Field(..., title="ID темы")
    topic_label: str = Field(..., title="Название темы")


class Topic(BaseModel):
    """
    Информация о темах документа с 1 по 4 уровень
    """

    lvl1: TopicInfo = Field(..., title="Тема уровня 1")
    lvl2: TopicInfo = Field(..., title="Тема уровня 2")
    lvl3: TopicInfo = Field(..., title="Тема уровня 3")
    lvl4: TopicInfo = Field(..., title="Тема уровня 4")
    probability: float = Field(..., title="Вероятность темы", ge=0, le=1)


class Document(BaseModel):
    document_id: int = Field(..., title="Уникальный ID документа")
    text: str = Field(..., title="Текст документа")


class DocumentWithoutText(BaseModel):
    document_id: int = Field(..., title="Уникальный ID документа")
    nel: NelFeatures
    sentiment: List[int] = Field(..., title="Сентимент для каждой сущности из поля nel")
    topics: List[Topic] = Field(..., title="Список тем с 1 по 4 уровень для документа")
    ngrams: List[Ngram] = Field(..., title="Список н-грам с признаками для документа")


class DocumentWithFeatures(Document, DocumentWithoutText):
    ...


class DocumentWithAllFeatures(Document, DocumentWithoutText):
    sentences: Sentences


class ManipulationIn(Document):
    nel: NelFeatures
    ngrams: List[Ngram] = Field(..., title="Список н-грам с признаками для документа")
    sentiment: List[int] = Field(..., title="Сентимент для каждой сущности из поля ner")


class SemanticRole(BaseModel):
    """
    Семантические роли слов в документе
    """

    document_id: int = Field(..., title="Уникальный ID документа")
    lemmas: List[str] = Field(
        ..., title="Список лемматизированных слов, для которых извлечены их роли"
    )
    roles: List[str] = Field(..., title="Список ролей для лемм из поля lemmas")

    # semantic_roles: SemanticRole

    # class Config:
    #     schema_extra = {
    #         "document_id": 204406080,
    #         "description": "Где-то в глубине души затеплилась надежда: а ну как в нашу петербургскую \"Норму\" будут приглашать гастролёров?",
    #         "ner": {
    #             "tags": ["ORG"],
    #             "entity_substr": ["норму"],
    #             "entity_offsets": [[74, 79]],
    #             "sentences": ["Где-то в глубине души затеплилась надежда: а ну как в нашу петербургскую \"Норму\" будут приглашать гастролёров?"],
    #             "sentences_offsets": [[0, 110]]
    #         },
    #         "nel": {

    #         }
    #     }
