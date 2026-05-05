# Team Task Manager

A backend system built using FastAPI for managing projects and tasks with authentication and role-based access control.

## Features
- JWT Authentication (Signup/Login)
- Project creation and management
- Task assignment and tracking
- Role-Based Access Control (RBAC)
- Dashboard (total, completed, pending, overdue tasks)

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## API Endpoints
- POST /signup
- POST /login
- GET /me
- POST /projects
- POST /tasks
- PATCH /tasks/{task_id}
- GET /dashboard

## Live Demo
https://web-production-52cd7.up.railway.app  
https://web-production-52cd7.up.railway.app/docs

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
