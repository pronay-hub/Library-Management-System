📚 Library Management System

A desktop-based Library Management System built with Python, Tkinter, and SQLite. The application helps an administrator manage books and students, record book issues and returns, and monitor overdue books through a graphical user interface.

📌 Table of Contents
- Overview
- Features
- Technology Stack
- Application Workflow
- Database Design
- Project Structure
- Installation and Setup
- How to Use
- Default Admin Login
- Future Improvements

📝 Overview
The Library Management System is designed to simplify routine library operations. An administrator can log in to the application and manage book records, student information, and book transactions.

The application uses Tkinter for its desktop GUI and SQLite for local data storage. The database file is created automatically when the application starts if it does not already exist.


✨ Features
- Admin Login — access the application through an administrator login.
- Book Management — add, view, update, delete, and search book records.
- Student Management — maintain student information.
- Issue Books — record when a book is issued to a student.
- Return Books — record returned books and update their availability.
- Overdue Tracking — view books that have passed their due date.
- SQLite Storage — store application data locally in a database.
🧰 Technology Stack
Technology	Purpose
Python	Main programming language
Tkinter	Desktop graphical user interface
SQLite	Local relational database
Git & GitHub	Version control and project hosting


🔄 Application Workflow
The diagram below shows the main flow of the application, from startup and login to dashboard operations and database updates.
```mermaid
flowchart TD
    A([Start Application]) --> B[Load Python Application]
    B --> C[Connect to SQLite Database]
    C --> D[Create Tables if Needed]
    D --> E[Display Admin Login]
    E --> F{Are Login Details Valid?}
    F -- No --> G[Show Login Error]
    G --> E
    F -- Yes --> H[Open Admin Dashboard]

    H --> I{Choose an Operation}
    I --> J[Book Management]
    I --> K[Student Management]
    I --> L[Issue Book]
    I --> M[Return Book]
    I --> N[View Overdue Books]
    I --> O[Logout]

    J --> J1[Add / View / Update / Delete / Search Books]
    K --> K1[Add / View / Update / Delete / Search Students]
    L --> L1[Select Student and Available Book]
    M --> M1[Select Issued Book and Record Return]
    N --> N1[Check Due Dates]

    J1 --> P[(SQLite Database)]
    K1 --> P
    L1 --> P
    M1 --> P
    N1 --> P

    P --> H
    O --> Q([Close Application])



Workflow Explanation
1. Application Startup: The Python application starts and connects to the SQLite database.
2. Database Initialization: Required tables are created if they do not already exist.
3. Admin Login: The administrator enters login credentials.
4. Dashboard: After successful login, the main dashboard is displayed.
5. Library Operations: The administrator can manage books and students, issue or return books, and view overdue records.
6. Database Updates: Changes made through the application are stored in the SQLite database.
7. Logout: The administrator can log out and close the application.
🗄️ Database Design
The application uses SQLite for local data storage. The database setup creates the following tables:
Table	Purpose
admins	Stores administrator login information
books	Stores book details and availability information
students	Stores student details
issue_records	Stores book issue and return transaction records


Note: The exact columns and relationships are defined in database.py.



📁 Project Structure
Library-Management-System/
│
├── main.py          # Main application and Tkinter GUI
├── database.py      # SQLite connection and table creation
├── README.md        # Project documentation
├── .gitignore       # Files excluded from Git tracking
└── library.db       # Created locally when the application runs
library.db is intentionally excluded from GitHub by .gitignore. Each user can generate their own local database by running the application.


⚙️ Installation and Setup
Prerequisites
- Python 3 installed
- Git (optional, for cloning the repository)
1. Clone the Repository
git clone https://github.com/pronay-hub/Library-Management-System.git
2. Open the Project Folder
cd Library-Management-System
3. Run the Application
python main.py
The application should initialize the SQLite database and open the login window.
Tkinter note: Tkinter is included with many standard Python installations. If the application reports that Tkinter is unavailable, install or repair the Tk support for your Python distribution.



🖥️ How to Use
1. Run main.py.
2. Log in using the administrator credentials configured in the project.
3. Use the dashboard to open the required section.
4. Add or manage books and student records.
5. Record book issues and returns.
6. Check the overdue section when required.
7. Log out when finished.



🚀 Future Improvements
- Role-based access for librarians and administrators
- Password hashing and stronger authentication
- Book issue due-date reminders
- Fine calculation for late returns
- Export reports to CSV or PDF
- Improved dashboard analytics and charts
- Automated database backup and restore


👨‍💻 Author
Pronay Gaine,Tanmoy Giri,Proloy Sadhukhan,Md.Toufiq Ahamed

GitHub: @pronay-hub
⭐ If you find this project useful, consider giving the repository a star.