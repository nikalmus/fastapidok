from fastapi import APIRouter
 
from app.api.routes.cleanings import router as cleanings_router
from app.api.routes.cleaner import router as cleaner_router
 
 
router = APIRouter()
 
 
router.include_router(cleanings_router, prefix="/cleanings", tags=["cleanings"])
router.include_router(cleaner_router, prefix="/cleaner", tags=["cleaner"])