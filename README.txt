Project: Team Task Manager

Description:
A full-stack task management backend built using FastAPI. The system supports user authentication, project creation, task assignment, and progress tracking with role-based access control.

Features:

* JWT-based Authentication (Signup/Login)
* Project Creation and Management
* Task Creation and Assignment
* Role-Based Access Control (only assigned users can update tasks)
* Dashboard with task summary (total, completed, pending, overdue)

Tech Stack:

* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn

API Endpoints:

* POST /signup
* POST /login
* GET /me
* POST /projects
* POST /tasks
* PATCH /tasks/{task_id}
* GET /dashboard

Deployment:

* Hosted on Railway

Live URL:
https://web-production-52cd7.up.railway.app

API Docs:
https://web-production-52cd7.up.railway.app/docs
