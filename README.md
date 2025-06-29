# Django DRF Message Board

A modern, API-driven message board built with Django, Django REST Framework, and PostgreSQL.  
Supports user registration, OTP-based login with JWT authentication.
---

## Features

- **User Registration**: Register with email and password via API.
- **OTP Login**: Login using email-based OTP; on successful verification, receive JWT access and refresh tokens.
- **JWT Authentication**: All protected endpoints require a valid JWT access token.
- **Message Board**: 
  - Post messages (authenticated users).
  - View all messages.
  - Edit and delete only your own messages.
  - Responsive UI using HTML + JavaScript (fetch/AJAX) that consumes the API.
- **Admin Panel**: Django admin for user and message management.
- **Swagger/OpenAPI**: API documentation available at `/swagger/`.
- **Dockerized**: Easy setup with Docker and Docker Compose.
- **Environment Variables**: All sensitive settings managed via `.env` file.

---

## Project Structure

```
drf-msg-board/
├── config/              # Django project settings
├── messagesapp/         # Message board app (models, APIs)
├── users/               # User management (models, APIs)
├── static/              # Static files (CSS, JS, images)
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env
├── Pipfile
├── README.md
└── swagger_urls.py

```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Nikhil7709/drf-msg-board.git
cd drf-msg-board
```

### 2. Create and Configure `.env`

Create a `.env` file in the project root:

```
DB_NAME=drfmsgdb
DB_USER=drfuser
DB_PASSWORD=drfpass
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Build and Run with Docker

```bash
docker-compose up --build
```

- The backend will be available at: [http://localhost:8000/](http://localhost:8000/)
- Django admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 4. Run Migrations and Create Superuser

In a new terminal:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## API Usage

### Registration

- **POST** `/api/register/`
  ```json
  {
    "email": "user@gmail.com",
    "password": "yourpassword"
  }
  ```

### OTP Login

- **POST** `/api/send-otp/`
  ```json
  { "email": "user@example.com" }
  ```
- **POST** `/api/verify-otp/`
  ```json
  { "email": "user@example.com", "otp": "123456" }
  ```
  - Returns: `{ "access": "...", "refresh": "..." }`

### Messages

- **GET** `/api/messages/`  
  List all messages (JWT required)
- **POST** `/api/messages/`  
  Create a message (JWT required)
- **GET** `/api/messages/<id>/`  
  Retrieve a specific message (JWT required)
- **PUT/PATCH** `/api/messages/<id>/`  
  Update your message (JWT required)
- **DELETE** `/api/messages/<id>/`  
  Delete your message (JWT required)

### Logout

- **POST** `/api/logout/`  
  Blacklists the refresh token.

---

---

## Development

- To install dependencies locally:  
  `pip install pipenv && pipenv install`
- To run locally without Docker, set up PostgreSQL and configure your `.env` accordingly.

---

## License

MIT License

---

## Author

- [Your Name](https://github.com/Nikhil7709)

---

## Acknowledgements

- Django & Django REST Framework
- Docker