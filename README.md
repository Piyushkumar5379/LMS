# Library Management System

A simple web-based library management system built with Flask, SQLAlchemy, and Bootstrap.

## Features

- User registration and login
- Book catalog management
- Borrowing and returning books
- Admin panel for adding books
- User profile to view borrowed books

## Installation

1. Install Python 3.7 or higher.
2. Clone or download the project.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5000/`

## Usage

- Register a new account or login.
- Browse available books on the home page.
- Borrow books if available.
- View your profile to see borrowed books and return them.
- Admin users (email: admin@library.com) can add new books.

## Database

The application uses SQLite database (`library.db`) which is created automatically on first run.

## Admin Access

To create an admin user, register with email `admin@library.com`.