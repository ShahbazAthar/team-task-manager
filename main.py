from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import models, schemas
from jose import jwt
from database import engine, Base, get_db
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from auth import get_current_user
from fastapi import Body
from pydantic import BaseModel
from datetime import datetime




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "API is running"}


SECRET_KEY = "secret123"
ALGORITHM = "HS256"

@app.get("/me")
def get_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        token = authorization.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(models.User).filter(models.User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    


class ProjectCreate(BaseModel):
    name: str


@app.post("/projects")
def create_project(
    project: ProjectCreate,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    new_project = models.Project(
        name=project.name,
        created_by=user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "id": new_project.id,
        "name": new_project.name,
        "created_by": user_id
    }



@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    # (simple check) project exists
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "status": new_task.status
    }

@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    update: schemas.TaskUpdate,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # RBAC: only assigned user can update
    if task.assigned_to != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    task.status = update.status
    db.commit()

    return {
        "message": "Task updated",
        "status": task.status
    }



@app.get("/dashboard")
def get_dashboard(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    tasks = db.query(models.Task).filter(models.Task.assigned_to == user_id).all()

    total = len(tasks)
    completed = len([t for t in tasks if t.status == "done"])
    pending = len([t for t in tasks if t.status != "done"])
    overdue = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"])

    return {
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    }