# 🧑‍💻 User Management App  

A **full-stack user management system** built with **FastAPI, Pydantic, and TailwindCSS**.  
It demonstrates **production-grade patterns** like input validation, error handling, and clean architecture, while also delivering a responsive **UI for user onboarding and management**.  

This project showcases how a real-world **authentication & onboarding flow** could be implemented in production systems such as SaaS dashboards, admin panels, or e-commerce apps.  

---

## 🚀 Project Purpose  

Recruiters often ask: *Can you design systems that look like real production apps?*  
This project answers that by demonstrating:  

- ✅ **User onboarding workflow** (register, list, delete).  
- ✅ **Strong data validation** and error handling.  
- ✅ **Frontend + Backend integration** with APIs.  
- ✅ **Scalable design** (JSON now, SQL/NoSQL later).  

---

## 🛠️ Tech Stack  

| Layer        | Technology | Why Used |
|--------------|------------|----------|
| **Backend**  | FastAPI    | Async APIs, built-in docs, production-ready |
|              | Pydantic   | Strict validation for user input |
| **Frontend** | TailwindCSS| Responsive, modern UI without custom CSS |
|              | Vanilla JS | Lightweight Fetch API integration |
| **Storage**  | JSON File  | Demo simplicity, DB-agnostic design |

> ⚡ Easily swappable with PostgreSQL, MongoDB, or MySQL for production.

---

## ✨ Features  

- **🔐 User Registration with Validations**  
  - Emails restricted to Gmail/Hotmail.  
  - Phone numbers validated with regex (`+1234567890`).  
  - Password strength rules enforced.  
  - Age auto-computed from Date of Birth.  

- **📡 REST Endpoints**  
  - `POST /users` → Register new user.  
  - `GET /user/` → Fetch all users.  
  - `DELETE /users/{id}` → Delete user.  

- **🖥️ Frontend Integration**  
  - Tailwind-based **Register Form**.  
  - **User List Table** with real-time refresh.  
  - **Delete Action** with confirmation.  
  - Toast-style **success/error messages**.  

---

## 🏗️ Architecture & Design Choices  

- **Separation of Concerns**: Models, validators, and CRUD logic decoupled.  
- **DB-Agnostic Storage**: JSON used for simplicity → can migrate to SQL/NoSQL.  
- **Error Handling**: `HTTPException` with clear messages & status codes.  
- **Security Hints**: Strong password policy, unique email checks, domain restrictions.  

---

## 🎨 UI Preview  

### Registration Form  
![Register Form](https://github.com/Naveed101633/FastAPI/blob/main/f1.png)  
![Register Form](https://github.com/Naveed101633/FastAPI/blob/main/f2.png)  

### User List Table  
![User List](https://github.com/Naveed101633/FastAPI/blob/main/form.png)  

*(UI built with TailwindCSS for responsive, clean design)*  

---

## ⚙️ Requirements & Execution:  
1️⃣  
```terminal:
uv runuvicorn main:app --reload
pip install -r requirements.txt
