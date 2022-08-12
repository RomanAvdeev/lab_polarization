import math
import random
from typing import List, Optional

from fastapi import APIRouter, Body

from api.api_v1.examples.examples import document_without_text
from polarization.schemas.polarization import Metrics
from schemas.document import DocumentWithoutText
from schemas.polarization import DocumentPolarization, TopicPolarization

router = APIRouter()


def softmax(x: List[float]) -> List[float]:
    x_max = max(x)
    e_x = [math.exp(v - x_max) for v in x]
    e_x_sum = sum(e_x)
    return [v / e_x_sum for v in e_x]


@router.post("/", response_model=List[TopicPolarization])
async def polarization(
    documents: List[DocumentWithoutText] = Body(..., example=[document_without_text.dict()])
) -> List[TopicPolarization]:
    unqiue_topic_ids = {topic.lvl3.id for d in documents for topic in d.topics}
    topics_polarization = []

    for topic_id in unqiue_topic_ids:
        num_poles = random.randint(2, 5)
        topic_docs, topic_entities, topic = [], set(), None
        for doc in documents:
            if any(t.lvl3.id == topic_id for t in doc.topics):
                if topic is None:
                    topic = next(t for t in doc.topics if t.lvl3.id == topic_id)

                neutral_prob, irrelevant_prob = random.random(), random.random()
                is_neutral = neutral_prob >= 0.9
                is_irrelevant = not is_neutral and irrelevant_prob >= 0.9
                if not is_irrelevant:
                    irrelevant_prob = max(0, irrelevant_prob - 0.1)

                topic_entities.update(doc.nel.entities)
                doc_polarization = DocumentPolarization(
                    document_id=doc.document_id,
                    probabilities=softmax([random.random() for _ in range(num_poles)]),
                    neutral=is_neutral,
                    neutral_prob=neutral_prob,
                    irrelevant=is_irrelevant,
                    irrelevant_prob=irrelevant_prob,
                )
                topic_docs.append(doc_polarization)

        num_ners = min(5, len(topic_entities))
        topics_polarization.append(
            TopicPolarization(
                documents_polarization=topic_docs,
                num_poles=num_poles,
                poles_names=[f"Полюс {i}" for i in range(1, num_poles + 1)],
                polarization_ner=random.sample(list(topic_entities), num_ners),
                entities_relations_to_poles=[
                    softmax([random.random() for _ in range(num_poles)]) for _ in range(num_ners)
                ],
                topic=topic,
                tension=random.random() * 10,
                significance=random.random() * 15,
            )
        )
    return topics_polarization

@router.post("/metrics", response_model=Metrics)
async def polarization(
    documents: Optional[List[DocumentWithoutText]] = Body(default=None, example=[document_without_text.dict()])
) -> Metrics:
    return Metrics(precision=0, recall=0, f1_score=0)
