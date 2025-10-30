# User Authentication Setup - Quick Guide

## What's Been Created

### Templates (in `templates/` folder)
1. **base.html** - Base template with navigation bar
2. **login.html** - Clean, simple login page
3. **home.html** - Protected home page (requires login)

### Views (in `user/views.py`)
1. **login_view** - Handles user authentication
2. **logout_view** - Handles user logout (POST only for security)
3. **home_view** - Protected home page (requires authentication)

### URL Configuration
- `/` - Home page (login required)
- `/login/` - Login page
- `/logout/` - Logout (POST only)
- `/admin/` - Django admin

## Testing the Setup

### 1. Create a superuser (if you haven't already)
```cmd
python manage.py createsuperuser
```

### 2. Run the development server
```cmd
python manage.py runserver
```

### 3. Test the login flow
- Visit http://127.0.0.1:8000/
- You'll be redirected to the login page (since home requires authentication)
- Login with your superuser credentials
- You'll see the home page with your user information

## Features Included

✅ Session-based authentication (as requested)
✅ Simple, clean design with gradient background
✅ Responsive layout
✅ CSRF protection
✅ Login required decorator on home page
✅ Success/error messages
✅ Navbar shows username when logged in
✅ Secure logout (POST only to prevent CSRF)
✅ Next URL redirect support (for protected pages)

## Security Features
- All forms include CSRF tokens
- Logout requires POST method
- Sessions are HTTP-only cookies
- Login redirects work with "next" parameter
- @login_required decorator protects sensitive views
