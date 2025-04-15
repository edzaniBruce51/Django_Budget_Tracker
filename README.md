# Personal Budget Tracker

A Django-based personal budget tracking system that helps users track expenses, manage budgets, and analyze spending patterns.

## Features

- Expense tracking with categorization
- Budget management with progress monitoring
- Monthly spending analysis with charts
- User authentication and data isolation
- Responsive dashboard interface

## Technical Stack

- Django 5.2
- SQLite database | choose this both in development and in deployment because it doesn't need too  much configurations to be done and my application is not going to scale and also it doesn't handle too much traffic.
- Chart.js for data visualization 
- Responsive CSS design

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   ```bash
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=False
   DJANGO_PORT=8000
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the server:
   ```bash
   python manage.py runserver 8000
   ```


## Security Considerations

- User data is isolated through user-specific queries
- CSRF protection enabled
- Debug mode disabled in production
- Secret key managed through environment variables
