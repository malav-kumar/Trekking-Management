Trekking Management System

A web-based Trekking Management System developed as a ModernApplication Development - I (MAD1) project.

The application provides separate functionality for Admin, Trek Staff,and Users (Trekkers). Administrators can manage users, staff, treksand bookings; staff can manage assigned treks; and users can browse andbook available treks.

Features

Admin

Admin login and dashboard

View registered users

View and manage staff

Create, edit and delete treks

Assign staff members to treks

View bookings

Manage user/staff access and status

Trek Staff

Staff login and dashboard

View assigned treks

Update available trek slots

Update trek status

View participants/bookings for assigned treks

User / Trekker

User registration and login

View available treks

Search treks by location

Filter treks by difficulty

Book a trek

View booking history

Edit profile details

Duplicate booking prevention

Additional Features

Flash messages for success and error feedback

Role-based access control

Bootstrap-based interface

Form and booking validation

SQLite database created programmatically using SQLAlchemy

Technology Stack

Technology   Purpose

Python       Programming languageFlask        Backend web frameworkJinja2       Server-side templatingHTML         Page structureCSS          StylingBootstrap    User interfaceSQLAlchemy   ORM and database interactionSQLite       Database

Project Structure

trekking_management_25F3002905/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── requirements.txt
├── .gitignore
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── admin_dashboard.html
    ├── assign_staff.html
    ├── assigned_treks.html
    ├── available_treks.html
    ├── base.html
    ├── booking_history.html
    ├── create_trek.html
    ├── edit_profile.html
    ├── edit_trek.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── staff_dashboard.html
    ├── update_slots.html
    ├── update_status.html
    ├── user_dashboard.html
    ├── view_bookings.html
    ├── view_participants.html
    ├── view_staff.html
    ├── view_treks.html
    └── view_users.html

Installation and Setup

1. Clone the repository

git clone https://github.com/malav-kumar/25F3002905.git
cd 25F3002905

2. Create a virtual environment

On Windows:

python -m venv venv

3. Activate the virtual environment

PowerShell:

venv\Scripts\Activate.ps1

Command Prompt:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run the application

python app.py

Open:

http://127.0.0.1:5000

Database

The project uses SQLite with SQLAlchemy.

The database is created programmatically by the application. The localdatabase file is excluded from Git using .gitignore.

User Roles

Admin: Manages users, staff, treks, staff assignments and bookings.

Staff: Manages assigned treks, available slots, trek status andparticipants.

User: Browses available treks, searches and filters treks, makesbookings, views booking history and edits their profile.

Booking Flow

User Login
    ↓
View Available Treks
    ↓
Search / Filter
    ↓
Select Trek
    ↓
Book Trek
    ↓
Booking Confirmation
    ↓
Booking History

The system prevents a user from booking the same trek more than once.

Flash Messages

Flash messages provide feedback for actions such as successful login,registration, trek operations, staff assignment, booking, profileupdates and validation errors.

Development Notes

This project was developed as part of the MAD1 academic projectusing Flask, Jinja2, HTML, CSS, Bootstrap, SQLAlchemy and SQLite.

Author

Malav Kumar

GitHub: https://github.com/malav-kumar/25F3002905