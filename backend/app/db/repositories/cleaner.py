from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.cleaner import CleanerCreate, CleanerUpdate, CleanerInDB

CREATE_CLEANER_QUERY = """
    INSERT INTO cleaner (name)
    VALUES (:name)
    RETURNING id, name;
"""

GET_CLEANER_BY_ID_QUERY = """
    SELECT id, name
    FROM cleaner
    WHERE id = :id;
"""

GET_ALL_CLEANERS_QUERY = """
    SELECT id, name
    FROM cleaner;
"""

UPDATE_CLEANER_BY_ID_QUERY = """
    UPDATE cleaner
    SET name = :name
    WHERE id = :id
    RETURNING id, name;
"""


DELETE_CLEANER_BY_ID_QUERY = """
    DELETE FROM cleaner
    WHERE id = :id
    RETURNING id;
"""

class CleanersRepository(BaseRepository):
    """
    All database actions associated with the Cleaner resource
    """

    async def create_cleaner(self, *, new_cleaner: CleanerCreate) -> CleanerInDB:
        query_values = new_cleaner.dict()
        cleaner = await self.db.fetch_one(query=CREATE_CLEANER_QUERY, values=query_values)
        return CleanerInDB(**cleaner)
    
    async def get_cleaner_by_id(self, *, id: int) -> CleanerInDB:
        cleaning = await self.db.fetch_one(query=GET_CLEANER_BY_ID_QUERY, values={"id": id})

        if not cleaning:
            return None

        return CleanerInDB(**cleaning)
    
    async def get_all_cleaners(self) -> List[CleanerInDB]:
        cleaner_records = await self.db.fetch_all(query=GET_ALL_CLEANERS_QUERY)

        return [CleanerInDB(**l) for l in cleaner_records]
    
    async def update_cleaner(self, *, id: int, cleaner_update: CleanerUpdate) -> CleanerInDB:
        cleaner = await self.get_cleaner_by_id(id=id)

        if not cleaner:
            return None

        cleaner_update_params = cleaner.copy(update=cleaner_update.dict(exclude_unset=True))
        if cleaner_update_params.name is None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid cleaning type. Cannot be None.")

        try:
            updated_cleaner = await self.db.fetch_one(
                query=UPDATE_CLEANER_BY_ID_QUERY, values=cleaner_update_params.dict()
            )
            return CleanerInDB(**updated_cleaner)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid update params.")
    
    async def delete_cleaner_by_id(self, *, id: int) -> int:
        cleaner = await self.get_cleaner_by_id(id=id)

        if not cleaner:
            return None

        deleted_id = await self.db.execute(query=DELETE_CLEANER_BY_ID_QUERY, values={"id": id})

        return deleted_id
