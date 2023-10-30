from typing import Optional
from app.models.core import CoreModel
from app.models.core import IDModelMixin, CoreModel


class CleanerBase(CoreModel):
    """
    All common characteristics of our Cleaner resource
    """
    name: Optional[str]


class CleanerCreate(CleanerBase):
    name: str


class CleanerUpdate(CleanerBase):
    name: str


class CleanerInDB(IDModelMixin, CleanerBase):
    name: str


class CleanerPublic(IDModelMixin, CleanerBase):
    pass
