# Production Deployment Guide

This Django project is configured for production deployment with:
- Django REST Framework for API endpoints
- Django templates for traditional views
- SQLite3 database
- Gunicorn WSGI server
- Whitenoise for static file serving
- Environment-based configuration using python-decouple
- Session-based authentication

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY`: Generate a new secret key for production
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names (comma-separated)
- Security settings: Set to `True` when using HTTPS

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic
```

### 6. Run the Application

**Development:**
```bash
python manage.py runserver
```


## Configuration Details

### Django REST Framework
- **Authentication**: Session-based authentication
- **Permissions**: IsAuthenticatedOrReadOnly (default)
- **Renderers**: JSON and Browsable API
- **Pagination**: Page number pagination (10 items per page)

### Static Files
- **STATIC_URL**: `/static/`
- **STATIC_ROOT**: `staticfiles/` (for collected static files)
- **Storage**: Whitenoise with compression and manifest

### Security Settings
The following security settings are configured via environment variables:
- `CSRF_COOKIE_SECURE`: Set to `True` in production (HTTPS only)
- `SESSION_COOKIE_SECURE`: Set to `True` in production (HTTPS only)
- `SECURE_SSL_REDIRECT`: Redirect HTTP to HTTPS
- `SECURE_HSTS_SECONDS`: HTTP Strict Transport Security
- `SECURE_CONTENT_TYPE_NOSNIFF`: Prevent MIME type sniffing
- `SECURE_BROWSER_XSS_FILTER`: Enable XSS filter
- `X_FRAME_OPTIONS`: Set to `DENY` to prevent clickjacking

### Session Configuration
- **Engine**: Database-backed sessions
- **Cookie Age**: 2 weeks (1209600 seconds)
- **HttpOnly**: Enabled
- **SameSite**: Lax

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate and set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Enable all security settings (SSL, HSTS, etc.)
- [ ] Run `python manage.py check --deploy`
- [ ] Collect static files
- [ ] Set up proper database backups
- [ ] Configure logging
- [ ] Use environment variables for sensitive data
- [ ] Review and test authentication flows

## Useful Commands

```bash
# Check for deployment issues
python manage.py check --deploy

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run production server
gunicorn core.wsgi:application --config gunicorn_config.py
```

## Notes

- SQLite is suitable for small to medium applications. For larger applications, consider PostgreSQL or MySQL.
- Gunicorn is configured to use multiple workers based on CPU count.
- Whitenoise serves static files efficiently with compression and caching.
- All sensitive configuration is managed through environment variables.
