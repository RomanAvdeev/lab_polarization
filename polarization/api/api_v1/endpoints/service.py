from enum import Enum
from typing import Any, List

from fastapi import APIRouter, File, UploadFile

from schemas.document import DocumentWithFeatures

router = APIRouter()


class ModelType(str, Enum):
    manipulation = "manipulation"
    polarization = "polarization"


@router.get("/train_data", response_model=List[DocumentWithFeatures])
def get_train_data(num_docs: int) -> List[DocumentWithFeatures]:
    """
    Скачивание набора данных для размерки и переобучения модели
    """
    ...


@router.post("/update_model")
def update_model(model_type: ModelType, file: UploadFile = File(..., description="Файл модели")):
    """
    Загрузка новой версии модели
    """
    ...
