# Restaurant System - User Service 🍽️

## Overview
This is the User Service component of the Restaurant System, built using Django and Django REST Framework. It handles user authentication, authorization, and user management functionalities for the restaurant management system.

## Features
- User authentication and authorization
- JWT-based authentication
- User registration and profile management
- RESTful API endpoints
- Cross-Origin Resource Sharing (CORS) support

## Technology Stack
- Python 3.x
- Django 4.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Docker

## Prerequisites
- Python 3.x
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (if running locally)

## Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd RestaurantSystem/user_service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t user-service .
```

2. Run the container:
```bash
docker run -p 8000:8000 user-service
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout

### User Management Endpoints
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `DELETE /api/users/profile/` - Delete user account

## Security
- JWT-based authentication
- Password hashing
- CORS protection
- Environment variable-based configuration

## Contributing
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please contact [contact information]

