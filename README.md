# Customer Support Ticketing System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Guidelines](#project-guidelines)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Database Setup](#database-setup)
    - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction
This project is a web-based **Customer Support Ticketing System** designed to streamline communication between customers and support teams. It provides a secure and user-friendly application where customers can easily raise support tickets, track their status, and receive updates. Concurrently, it empowers support teams with efficient tools to manage and resolve these tickets effectively.

The primary goal of this application is to enhance customer satisfaction by offering a transparent and organized channel for support, while boosting the productivity of the support staff.

## Features
*   **Secure User Authentication:** Robust customer registration and login system.
*   **Ticket Submission:** Customers can easily create and submit new support tickets with details and categories.
*   **Ticket Tracking:** Users can view a history of their submitted tickets and monitor their real-time status (e.g., Open, In Progress, Closed).
*   **Admin/Agent Dashboard:**
    *   **Comprehensive Ticket View:** Administrators and support agents can view all submitted tickets.
    *   **Ticket Management:** Assign tickets to specific agents, update ticket status, and add internal notes/comments.
    *   **User Management:** Admin controls for managing user accounts (creating/deactivating users, assigning roles).
*   **Role-Based Access:** Distinct functionalities and dashboards for customers and support personnel.
*   **Search and Filter:** Efficiently search and filter tickets by status, category, agent, or customer.
*   **Email Notifications:** (Planned/Implemented) Automated email notifications for ticket status changes or new comments.
*   **File Attachments:** (Planned/Implemented) Customers and agents can attach relevant files to tickets.

## Project Guidelines
*   **Timeline:** 55 days
*   **Monitoring:** Progress review every 30 days
*   **Submission:** Push all code to GitHub with documentation
*   **Documentation:** Include setup steps, screenshots, and user instructions
*   **Presentation:** PPT summarizing functionality, architecture, and screenshots

## Technologies Used
*   **Backend:**
    *   Python **3.9+**
    *   Flask **2.3.x**
    *   Flask-SQLAlchemy **3.1.x**
    *   PyMySQL **1.0.x**
    *   Flask-Login (for user session management)
    *   Flask-WTF (for form handling and CSRF protection)
    *   Werkzeug (part of Flask, for security utilities)
*   **Frontend:**
    *   HTML5
    *   CSS3 (Utilizing **Bootstrap 5** for responsive design and styling)
    *   JavaScript (for dynamic elements like form validation, AJAX updates, etc.)
*   **Database:**
    *   MySQL **8.0**
*   **Version Control:** Git & GitHub

## Setup Instructions

### Prerequisites
Before you begin, ensure you have the following installed on your system:
*   **Python:** **3.9 or higher** ([Download Python](https://www.python.org/downloads/))
*   **pip:** Python package installer (comes with Python)
*   **Git:** ([Download Git](https://git-scm.com/downloads))
*   **MySQL Server:** **8.0** ([Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/))
*   **MySQL Client:** Command-line client or GUI tool like MySQL Workbench.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/likhitha9966/ticketing-system.git
    cd ticketing-system
    ```

2.  **Create and activate a Python virtual environment:**
    *   **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Make sure you have created a `requirements.txt` file by running `pip freeze > requirements.txt` in your activated venv.)*

### Database Setup

1.  **Start your MySQL server.**
    *   (Windows: Services -> MySQL80 -> Start)
    *   (macOS: `brew services start mysql` or System Preferences -> MySQL)
    *   (Linux: `sudo systemctl start mysql`)

2.  **Access your MySQL server** (e.g., via MySQL command-line client or Workbench).
    ```bash
    mysql -u root -p
    ```
    (Enter my MySQL root password when prompted)

3.  **Create the database for the project:**
    ```sql
    CREATE DATABASE ticketing_system_db;
    ```

4.  **Exit MySQL client:**
    ```bash
    exit
    ```

5.  **Configure your database connection string:**
    *   Open your `app.py` or `config.py` file.
    *   Locate the `SQLALCHEMY_DATABASE_URI` variable.
    *   Update it to match your MySQL credentials.
        ```python
        # Example for app.py or config.py
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Likhitha%4069@localhost:3306/ticketing_system_db'
        ```
        *(Note: my password `Likhitha@69` has been URL-encoded as `Likhitha%4069` to handle the `@` character correctly.)*

6.  **Initialize database tables:**
    Run your Flask application once to create the necessary tables in `ticketing_system_db`.
    ```bash
    # In your project directory, with venv active
    set FLASK_APP=app.py         # On Windows
    set FLASK_ENV=development    # On Windows
    # export FLASK_APP=app.py    # On macOS/Linux
    # export FLASK_ENV=development # On macOS/Linux
    flask run
    ```
    The `db.create_all()` call in your application will create the tables. You can `Ctrl+C` to stop the server after this initial run if you just wanted to create tables.

### Running the Application

1.  **Ensure your MySQL server is running.**
2.  **In your terminal, navigate to the project root and activate your virtual environment.**
    ```bash
    cd ticketing-system
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # macOS/Linux
    ```
3.  **Set Flask environment variables:**
    ```bash
    set FLASK_APP=app.py         # Windows
    set FLASK_ENV=development    # Windows
    # export FLASK_APP=app.py    # macOS/Linux
    # export FLASK_ENV=development # On macOS/Linux
    ```
4.  **Start the Flask development server:**
    ```bash
    flask run
    ```

5.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/`

## Usage
*   **Customer Registration:** Navigate to `/register` to create a new customer account.
*   **Customer Login:** Access `/login` with your registered credentials.
*   **Customer Dashboard:** After logging in, customers can view a list of their submitted tickets and access an interface to create new tickets.
*   **Ticket Submission:** Fill out the ticket form (title, description, category, etc.) and submit.
*   **Admin/Agent Access:** To access the administrative or agent functionalities, a user's role/flag will need to be configured in the database (e.g., setting an `is_admin` or `role` column for a specific user in the `users` table). Once logged in as an admin/agent, you will have access to dashboards to view all tickets, assign them, and update their statuses.

## Screenshots
# Ticketing System Project

## Screenshots

*   **Home Page:**
    ![Home Page Screenshot](screenshots/homepage.png)

*   **User Registration Page:**
    ![User Registration Screenshot](screenshots/user_registration.png)

*   **User Login Page:**
    ![User Login Screenshot](screenshots/user_login.png)

*   **Customer Dashboard (Viewing Tickets):**
    ![Customer Dashboard Screenshot](screenshots/customer_dashboard_tickets.png)

*   **Ticket Submission Form:**
    ![Ticket Submission Form Screenshot](screenshots/ticket_submission_form.png)

*   **Admin/Agent Dashboard (All Tickets View):**
    ![Admin Dashboard Screenshot](screenshots/admin_dashboard_all_tickets.png)

*   **Home Page:**