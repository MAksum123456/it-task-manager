# IT Task Manager

A web-based application for managing tasks within team projects, with a flexible access control system.

---

## 📚 Table of Contents

* [About the Application](#about-the-application)
* [Main Technologies](#main-technologies)
* [Key Features](#key-features)
* [Installation](#installation)
* [Usage](#usage)
* [UI Screenshots](#ui-screenshots)
* [Additional Information](#additional-information)

---

## 📌 About the Application

**IT Task Manager** helps organize and manage tasks, workers, and projects effectively. It includes role-based access control and clearly defined entities:

### 🔸 Entities:

* **TaskType**: A category or type of task (e.g., *Bug*, *Feature*).
* **Task**: The core unit of work. Each task includes:

  * Name, Description, Deadline
  * Status (Completed/In Progress), Priority
  * Related TaskType, Assigned Worker, and Project
* **Worker**: A user assigned to tasks. Displays:

  * Username, Full Name, Position, Team
* **Position**: The job title of a worker (e.g., *Backend Developer*).
* **Team**: Represents a group that workers belong to.
* **Project**: Contains:

  * Name, Description, Start and End Dates, and Assigned Team

Each user has role-based permissions — only authorized users can create, modify, or delete tasks and related entities, ensuring secure and managed collaboration.

---

## 🚀 Main Technologies

* Python
* Django
* PostgreSQL (Production)
* SQLite (Development)
* HTML5 / CSS3
* Bootstrap

---

## 🛠️ Key Features

* Full **CRUD** support for tasks, task types, workers, projects, teams, and positions
* Role-based access:

  * **Administrator**, **HR**, **Project Manager**, **Team Lead**, **Employee**
* Permission-controlled UI (e.g., buttons are disabled for users without permission)
* Clean and user-friendly interface
* Team and worker assignment per project

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/MAksum123456/it-task-manager.git

# 2. Navigate into the directory
cd it-task-manager

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run migrations
python manage.py migrate

# 7. Create a superuser
python manage.py createsuperuser

# 8. Start the development server
python manage.py runserver
```

📌 **Note:** SQLite is used for local development. PostgreSQL is recommended for production.

---

## 🌐 Usage

1. Open your browser and go to `http://127.0.0.1:8000/`.
2. Log in using your superuser credentials or register a new user.
3. Use the navigation bar to access features such as managing tasks, workers, and projects.

---

## 🖼 UI Screenshots

### 🔹 Diagram

![Diagram](https://github.com/user-attachments/assets/47a37a83-0adf-4b93-9451-ab442c211edd)

### 🔹 Home Page

![Home](https://github.com/user-attachments/assets/18e199dc-21f3-4bdd-baf9-b02048d62e07)

### 🔹 List Views

* ![Task Type List](https://github.com/user-attachments/assets/24518225-5e3a-4cb6-ab8b-844a116def89)
* ![Task List](https://github.com/user-attachments/assets/615e2142-5412-481e-8059-a2c83ea9c5ce)
* ![Worker List](https://github.com/user-attachments/assets/1d3f7197-0a88-4b3a-8772-640312ce00c2)
* ![Position List](https://github.com/user-attachments/assets/5ec41914-5645-4eec-a271-bc2910371c41)
* ![Project List](https://github.com/user-attachments/assets/179a9875-b1a2-4473-afa9-ced246b200a6)
* ![Team List](https://github.com/user-attachments/assets/b518029e-93ae-4584-b96e-410a242f4adb)

### 🔹 Detail Views

* ![Task Type Detail](https://github.com/user-attachments/assets/80d78aa0-2905-4943-8c93-06c5e6c0bd00)
* ![Task Detail](https://github.com/user-attachments/assets/4550cf1c-83a4-465d-b6f8-ac53464efb47)
* ![Worker Detail](https://github.com/user-attachments/assets/8b6be40a-55d2-4f37-8b66-f63e63dfe3af)
* ![Position Detail](https://github.com/user-attachments/assets/34b6205a-7f70-424d-9697-5a3e1031433e)
* ![Project Detail](https://github.com/user-attachments/assets/5030de6f-418b-4442-9299-a6b1d0edfc17)
* ![Team Detail](https://github.com/user-attachments/assets/571a4d10-0eaa-4f49-a9bd-ed944b9d80ef)

### 🔹 Forms

* ![Create Task Type](https://github.com/user-attachments/assets/ac61bb69-f0ab-40be-8a32-de3f8812cd45)
* ![Create Task](https://github.com/user-attachments/assets/1cc4392d-b959-4390-8e69-4e60cb39a876)
* ![Create Worker](https://github.com/user-attachments/assets/413b9581-cd61-4b32-a4ea-cef7c2cb9dcb)
* ![Create Position](https://github.com/user-attachments/assets/71cdc462-920c-4548-9e3a-4c64b3c9bc0f)
* ![Create Project](https://github.com/user-attachments/assets/47f6baa1-1aeb-4600-bc8e-22b2a57f8cfb)
* ![Create Team](https://github.com/user-attachments/assets/72622d45-e17b-4620-9df7-e874eac8773c)

### 🔹 Other

* ![Delete Form](https://github.com/user-attachments/assets/aa3fca6f-b05d-4022-bf81-55b15e0c81cd)
* ![Improved Create Forms](https://github.com/user-attachments/assets/1d0e4cea-d353-4844-b881-1c55e1bfc185)
* ![Extra Info](https://github.com/user-attachments/assets/c03b5ffe-0e76-4fdb-bfac-035676dbf54f)

### 🔹 Registration/Login

* ![Register](https://github.com/user-attachments/assets/c0e88839-b138-434f-86f0-21cab8398d12)
* ![Login](https://github.com/user-attachments/assets/2355017b-530e-4acf-8e5a-58884c252649)

---

## ℹ️ Additional Information

* The system uses Django's built-in authentication and permission framework.
* Role and access control are enforced both at the UI and database level.
* Designed for teams managing software projects, but flexible for other domains.

---

Feel free to contribute or submit issues!

