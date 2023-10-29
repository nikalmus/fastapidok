from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB
from typing import Optional
import logging
CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type, cleaner_id)
    VALUES (:name, :description, :price, :cleaning_type, :cleaner_id)
    RETURNING id, name, description, price, cleaning_type;
"""
 
class CleaningsRepository(BaseRepository):
    """"
    All database actions associated with the Cleaning resource
    """
 
    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningInDB:
        #logger = logging.getLogger(__name__)
        query_values = new_cleaning.dict()
        cleaning = await self.db.fetch_one(query=CREATE_CLEANING_QUERY, values=query_values)
        # logger.debug("Validating cleaner_id is present before creating cleaning...")
  
        # if not new_cleaning.cleaner_id:
        #     logger.error("cleaner_id is missing from CleaningCreate")
        #     raise ValueError("cleaner_id is required")
 
        return CleaningInDB(**cleaning)