from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assigned_to: int
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    status: str