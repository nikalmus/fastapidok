from typing import List

from fastapi import APIRouter, Body, Depends, Path, HTTPException 
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.cleaner import CleanerCreate, CleanerUpdate, CleanerPublic
from app.db.repositories.cleaner import CleanersRepository  # Adjust the import as needed
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.get("/", response_model=List[CleanerPublic], name="cleaners:get-all-cleaners")
async def get_all_cleaners(
    cleaners_repo: CleanersRepository = Depends(get_repository(CleanersRepository)),
) -> List[CleanerPublic]:
    return await cleaners_repo.get_all_cleaners()

@router.get("/{id}/", response_model=CleanerPublic, name="cleaner:get-cleaning-by-id")
async def get_cleaner_by_id(
    id: int, cleaners_repo: CleanersRepository = Depends(get_repository(CleanersRepository))
) -> CleanerPublic:
    cleaner = await cleaners_repo.get_cleaner_by_id(id=id)

    if not cleaner:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaner found with that id.")

    return cleaner

@router.post("/", response_model=CleanerPublic, name="cleaners:create-cleaner", status_code=HTTP_201_CREATED)
async def create_new_cleaner(
    new_cleaner: CleanerCreate = Body(..., embed=True),
    cleaners_repo: CleanersRepository = Depends(get_repository(CleanersRepository)),
) -> CleanerPublic:
    created_cleaner = await cleaners_repo.create_cleaner(new_cleaner=new_cleaner)
    return created_cleaner

@router.put("/{id}/", response_model=CleanerPublic, name="cleaner:update-cleaning-by-id")
async def update_cleaner_by_id(
    id: int = Path(..., ge=1, title="The ID of the cleaner to update."),
    cleaner_update: CleanerUpdate = Body(..., embed=True),
    cleanings_repo: CleanersRepository = Depends(get_repository(CleanersRepository)),
) -> CleanerPublic:
    updated_cleaning = await cleanings_repo.update_cleaner(id=id, cleaner_update=cleaner_update)

    if not updated_cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaner found with that id.")

    return updated_cleaning

@router.delete("/{id}/", response_model=int, name="cleaners:delete-cleaner-by-id")
async def delete_cleaner_by_id(
    id: int = Path(..., ge=1, title="The ID of the cleaner to delete."),
    cleaners_repo: CleanersRepository = Depends(get_repository(CleanersRepository)),
) -> int:
    deleted_id = await cleaners_repo.delete_cleaner_by_id(id=id)

    if not deleted_id:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaner found with that id.")

    return deleted_id