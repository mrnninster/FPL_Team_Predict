from pydantic import BaseModel
from typing import List

class CreatePlayer(BaseModel):
    name: str
    position: str
    playerSkills: List[dict]