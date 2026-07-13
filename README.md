# Task & Annotation Management API

A Django REST Framework backend for managing radiology tasks and annotating medical images with polygon-based annotations. Deployed on [Render](https://render.com).

## Tech Stack

- **Python 3.12**
- **Django 6.0**
- **Django REST Framework 3.17**
- **SimpleJWT** (authentication)
- **Cloudinary** (media storage)
- **WhiteNoise** (static files)
- **SQLite** (dev) / PostgreSQL 

## Project Structure

```
backend/
├── config/
│   ├── settings.py        # Project settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── apps/
│   ├── accounts/          # Custom user model, auth (register/login/profile)
│   ├── tasks/             # Task CRUD with Kanban statuses
│   └── annotation/        # Image upload + polygon annotation CRUD
├── media/                 # Uploaded media files
├── staticfiles/           # Collected static files
├── build.sh               # Render build script
├── manage.py              # Django management CLI
├── requirements.txt       # Python dependencies
└── runtime.txt            # Python version for Render
```

## Features

### Authentication
- Custom user model with email-based login
- JWT access/refresh token authentication (1-hour access, 7-day refresh)
- Register, login, and profile endpoints

### Task Management
- Full CRUD for tasks (create, read, update, delete)
- Three statuses: To Do, In Progress, Done (Kanban-ready)
- Three priority levels: Low, Medium, High
- Due date validation (no past dates)
- Tag support (max 5 per task)
- Filter tasks by date
- Each user only sees their own tasks

### Image Annotation
- Upload radiology images (stored locally or on Cloudinary)
- Create, view, and delete polygon annotations on images
- Polygon points stored as JSON coordinate arrays
- Labeled annotations per image
- Authenticated image file streaming
- Each user only accesses their own images and annotations

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/accounts/register/` | Register a new user | No |
| POST | `/api/accounts/login/` | Login and receive JWT tokens | No |
| POST | `/api/accounts/refresh/` | Refresh an access token | No |
| GET | `/api/accounts/profile/` | Get current user profile | Yes |

### Tasks

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/tasks/` | List tasks (optional `?date=YYYY-MM-DD`) | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/<id>/` | Retrieve a task | Yes |
| PUT | `/api/tasks/<id>/` | Full update a task | Yes |
| PATCH | `/api/tasks/<id>/` | Partial update (e.g. status drag-drop) | Yes |
| DELETE | `/api/tasks/<id>/` | Delete a task | Yes |

### Annotations

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/annotation/images/` | List uploaded images | Yes |
| POST | `/api/annotation/images/` | Upload an image (multipart) | Yes |
| GET | `/api/annotation/images/<id>/` | Get image metadata | Yes |
| DELETE | `/api/annotation/images/<id>/` | Delete an image | Yes |
| GET | `/api/annotation/images/<id>/file/` | Stream raw image file | Yes |
| GET | `/api/annotation/polygons/?image=<id>` | List polygons for an image | Yes |
| POST | `/api/annotation/polygons/` | Create a polygon | Yes |
| PUT | `/api/annotation/polygons/<id>/` | Full update a polygon | Yes |
| PATCH | `/api/annotation/polygons/<id>/` | Partial update a polygon | Yes |
| DELETE | `/api/annotation/polygons/<id>/` | Delete a polygon | Yes |

## Data Models

### User
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| email | EmailField | Used as `USERNAME_FIELD` |
| username | CharField | Required |

### Task
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| user | ForeignKey | CASCADE to User |
| title | CharField(255) | Min 3 characters |
| description | TextField | Optional |
| status | CharField | `todo` / `in_progress` / `done` |
| priority | CharField | `low` / `medium` / `high` |
| due_date | DateField | Cannot be in the past |
| tags | JSONField | List, max 5 items |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |

### UploadedImage
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| user | ForeignKey | CASCADE to User |
| image | ImageField | Uploaded to `uploads/` |
| uploaded_at | DateTimeField | Auto-set on creation |

### Polygon
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| image | ForeignKey | CASCADE to UploadedImage |
| label | CharField(100) | Optional |
| points | JSONField | Array of `[x, y]` coordinates |
| created_at | DateTimeField | Auto-set on creation |

## Setup

### Prerequisites

- Python 3.12+
- pip

### Local Development

```bash
# Clone the repository
git clone https://github.com/jannatulbakia/task_annotation_management.git
cd task_annotation_management/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your values

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | Yes | `True` for dev, `False` for production |
| `ALLOWED_HOSTS` | Yes | Comma-separated hostnames |
| `CORS_ALLOWED_ORIGINS` | Yes | Comma-separated frontend origins |
| `CSRF_TRUSTED_ORIGINS` | Yes | Comma-separated frontend origins |
| `CLOUDINARY_CLOUD_NAME` | No | Cloudinary cloud name (for media storage) |
| `CLOUDINARY_API_KEY` | No | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | No | Cloudinary API secret |

### Deploy to Render

1. Push to GitHub
2. Create a new **Web Service** on Render
3. Connect the repository
4. Set the build command to `./build.sh`
5. Set the start command to `gunicorn config.wsgi:application`
6. Add all environment variables in the Render dashboard

The `build.sh` script handles `pip install`, `collectstatic`, and `migrate` automatically.

## Authentication

All endpoints except register and login require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

## Admin Access

Email: admin@gmail.com
password: Admin123!

Tokens are obtained by:

1. `POST /api/accounts/register/` with `email`, `username`, `password`
2. `POST /api/accounts/login/` with `email`, `password` to receive `access` and `refresh` tokens
3. `POST /api/accounts/refresh/` with `refresh` to obtain a new `access` token

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 6.0.6 | Web framework |
| djangorestframework | 3.17.1 | REST API toolkit |
| djangorestframework-simplejwt | 5.5.1 | JWT authentication |
| django-cors-headers | 4.9.0 | Cross-origin request handling |
| django-cloudinary-storage | 0.3.0 | Cloudinary media storage |
| cloudinary | 1.44.1 | Cloudinary SDK |
| gunicorn | 26.0.0 | Production WSGI server |
| whitenoise | 6.12.0 | Static file serving |
| python-decouple | 3.8 | Environment variable management |
| pillow | 12.3.0 | Image processing |
| PyJWT | 2.13.0 | JSON Web Token library |
