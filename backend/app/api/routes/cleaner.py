from typing import List

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.models.cleaner import CleanerCreate, CleanerPublic
from app.db.repositories.cleaner import CleanersRepository  # Adjust the import as needed
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.get("/")
async def get_all_cleaners() -> List[dict]:
    # Replace with logic to retrieve all cleaners from the database
    cleaners = [
        {"id": 1, "name": "Cleaner 1"},
        {"id": 2, "name": "Cleaner 2"}
    ]
    return cleaners

@router.post("/", response_model=CleanerPublic, name="cleaners:create-cleaner", status_code=HTTP_201_CREATED)
async def create_new_cleaner(
    new_cleaner: CleanerCreate = Body(..., embed=True),
    cleaners_repo: CleanersRepository = Depends(get_repository(CleanersRepository)),
) -> CleanerPublic:
    created_cleaner = await cleaners_repo.create_cleaner(new_cleaner=new_cleaner)
    return created_cleaner
