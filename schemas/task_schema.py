from pydantic import BaseModel,Field,field_validator
from typing import Optional
import logging

logger = logging.getLogger(__name__)
class TaskCreate(BaseModel):
    task_id:int = Field(gt=0) #doubt 
    title:str = Field(min_length=3, max_length=100)
    description:str=Field(min)

    @field_validator("title")
    @classmethod
    def validate_title(cls,value):
        value=value.strip()
        if value:
            return value
        else:
            raise ValueError("title not valid")
    


class TaskUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None