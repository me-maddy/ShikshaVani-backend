# 🎓 Faculty Feedback Management Backend (FastAPI)

This is the backend API for a **Faculty Feedback System**, built with **FastAPI** and connected to **PostgreSQL** database.  
The system manages **Student** and **Faculty** authentication, **Classes**, **Subjects**, and **Student Feedback**.

---

## 🚀 Features

### 👩‍🎓 Student Side:

- **Register/Login** students.
- **Select Faculty** and **Class** during registration.
- **Provide feedback** on selected **Subjects** within the Class.

### 👩‍🏫 Faculty Side:

- **Register/Login** faculties.
- **Upload faculty name** and **email**.
- **Add multiple Classes** under their Faculty.
- **Add Subjects** under each Class.
- **View Feedback** received for each Subject and Class.

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL (NeonDB)
- **ORM:** SQLAlchemy
- **Authentication:** JWT Tokens
- **Hosting (for production):** Render / Railway

---

## 📂 Project Structure

- `/models`: Database Models (Faculty, Student, Class, Subject, Feedback)
- `/schemas`: Pydantic models (Request/Response Validation)
- `/routes`: API Endpoints (Student APIs, Faculty APIs, Feedback APIs)
- `/repository`: Database Queries
- `/services`: Business Logic
- `main.py`: FastAPI Application Entry Point
- `.env`: Environment variables (Database URL, JWT Secret)

---

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/me-maddy/ShikshaVani-backend.git
cd your-backend-repo
```
