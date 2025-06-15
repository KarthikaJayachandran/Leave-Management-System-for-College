# Leave-Management-System-for-College
To automate the process of requesting, approving, and tracking student leaves digitally through an online platform.

#Online Leave Management System for College 

A desktop-based application that enables students to apply for leave and faculty to manage 
leave requests digitally. This system is built using PyQt for the user interface and SQLite for 
the backend database. 
                                   
#Features 

Student Module 
- Student login/registration
- Submit leave requests with:
    - From date
    - To date
    - Reason
- Leave type (Sick, Casual, Other)
- View leave request status (Pending, Approved, Rejected)
  
                                      
#Faculty Module 
- Faculty login
- View list of student leave requests
- Approve or reject requests
- Optionally add review comments

#Technology Stack 

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | PyQt5 (Python GUI Framework)        |
| Backend     | Python 3.x                          |
| Database    | SQLite3                             |
| PDF/Export  | reportlab, pandas (optional)        |

## 🗂 Project Structure 
LeaveManagement/
│
├── main.py                 # Entry point of the application
├── db/
│   └── leave_system.db     # SQLite database file
│
└── README.md               # Project documentation

#How to Run the Project 

1. Clone this repository:
```bash 
git clone https://github.com/your-username/leave-management-pyqt.git 
cd leave-management-pyqt

2. (Optional but recommended) Create a virtual environment: 
python -m venv venv 
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies: 
pip install -r requirements.txt

4. Run the application: 
python main.py ---

Sample Login Credentials 
| Role      | Username | Password  |
|-----------|----------|-----------|
| Student   | AD1      | AD1@123   |
| Faculty   | T1       | T1@123    |


Database Schema Overview (SQLite)

Table: users

| Column Name | Type      | Description                     |
|-------------|-----------|---------------------------------|
| id          | INTEGER   | Primary Key                     |
| name        | TEXT      | User's name                     |
| email       | TEXT      | Unique login email              |
| password    | TEXT      | Hashed password                 |
| role        | TEXT      | 'student' or 'faculty'          |
  
Table: leave_requests 
  
```markdown
| Column Name   | Type      | Description                                      |
|---------------|-----------|--------------------------------------------------|
| id            | INTEGER   | Primary Key                                      |
| student_id    | INTEGER   | Foreign Key to `users` table                     | 
| from_date     | TEXT      | Leave start date (ISO format: `YYYY-MM-DD`)      |
| to_date       | TEXT      | Leave end date (ISO format: `YYYY-MM-DD`)        |
| reason        | TEXT      | Reason for leave                                 |
| leave_type    | TEXT      | `Sick` / `Casual` / `Other`                      |
| status        | TEXT      | `Pending` / `Approved` / `Rejected`              |
| reviewed_by   | INTEGER   | Foreign Key to `faculty` table (optional)        |
| comment       | TEXT      | Reviewer's remark                                |
```
  
    
Future Improvements 
  
Faculty comment notification to student 
Admin module with analytics 
Dark mode theme for UI 
Mobile version using Kivy or PyQt for Android 
  

License 
This project is licensed under the MIT License. Feel free to modify and distribute it. 
