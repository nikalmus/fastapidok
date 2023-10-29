from app.db.repositories.base import BaseRepository
from app.models.cleaner import CleanerCreate, CleanerInDB

CREATE_CLEANER_QUERY = """
    INSERT INTO cleaner (name)
    VALUES (:name)
    RETURNING id, name;
"""

class CleanersRepository(BaseRepository):
    """
    All database actions associated with the Cleaner resource
    """

    async def create_cleaner(self, *, new_cleaner: CleanerCreate) -> CleanerInDB:
        query_values = new_cleaner.dict()
        cleaner = await self.db.fetch_one(query=CREATE_CLEANER_QUERY, values=query_values)
        return CleanerInDB(**cleaner)
