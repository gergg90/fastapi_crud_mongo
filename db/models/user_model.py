from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    
    # No corre con servidor uvicorn
    id: Optional[str]

    # id: str | None # el campo id se define none (opcional)
    username: str
    full_name: str
    email: str