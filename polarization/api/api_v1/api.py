from fastapi import APIRouter

from api.api_v1.endpoints import polarization

api_router = APIRouter()
# api_router.include_router(
#     manipulation.router, prefix="/manipulation", tags=["Выявление манипулирования"]
# )
api_router.include_router(
    polarization.router, prefix="/polarization", tags=["Выявление поляризации"]
)
# api_router.include_router(
#     preprocessing.router, prefix="/feature_extractor", tags=["Подготовка данных"]
# )
# api_router.include_router(service.router, prefix="/service", tags=["Переобучение моделей"])
# api_router.include_router(
#     semantic_roles.router, prefix="/semantic_roles", tags=["Экстрактор семантических ролей"]
# )
