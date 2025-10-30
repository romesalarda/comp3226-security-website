# Deploying Django Project to Railway

## Current Project Status
✅ Production-ready Django project with:
- Django REST Framework
- Gunicorn (WSGI server)
- Whitenoise (static files)
- Environment-based configuration
- Session authentication
- SQLite database

## Deploy to Railway

### Prerequisites
1. Create a [Railway account](https://railway.app/)
2. Install Railway CLI (optional): `npm i -g @railway/cli`

### Option 1: Deploy via Railway Dashboard (Easiest)

1. **Push your code to GitHub**:
   ```cmd
   git init
   git add .
   git commit -m "Initial commit - production ready Django app"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create new project on Railway**:
   - Go to https://railway.app/
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Django and deploy!

3. **Configure Environment Variables** in Railway dashboard:
   - `SECRET_KEY` = (generate a new secret key)
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = your-app.railway.app
   - `CSRF_COOKIE_SECURE` = True
   - `SESSION_COOKIE_SECURE` = True
   - `SECURE_SSL_REDIRECT` = True
   - `SECURE_HSTS_SECONDS` = 31536000
   - `SECURE_HSTS_INCLUDE_SUBDOMAINS` = True
   - `SECURE_HSTS_PRELOAD` = True

4. **Deploy**:
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://your-app.railway.app`

### Option 2: Deploy via Railway CLI

1. **Login to Railway**:
   ```cmd
   railway login
   ```

2. **Initialize project**:
   ```cmd
   railway init
   ```

3. **Deploy**:
   ```cmd
   railway up
   ```

4. **Set environment variables**:
   ```cmd
   railway variables set SECRET_KEY="your-secret-key-here"
   railway variables set DEBUG="False"
   railway variables set ALLOWED_HOSTS="*.railway.app"
   ```

5. **Open your app**:
   ```cmd
   railway open
   ```

## Deploy to Other Platforms

### Render.com

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo
4. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn core.wsgi:application`
   - **Environment**: Python 3
5. Add environment variables (same as Railway)
6. Deploy!

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set buildpack: `heroku buildpacks:set heroku/python`
5. Set environment variables:
   ```cmd
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS=".herokuapp.com"
   ```
6. Deploy: `git push heroku main`
7. Run migrations: `heroku run python manage.py migrate`
8. Create superuser: `heroku run python manage.py createsuperuser`

### DigitalOcean App Platform

1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Select GitHub repo
4. Configure:
   - **Resource Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Run Command**: `gunicorn core.wsgi:application`
5. Add environment variables
6. Deploy!

## Important Notes for Production

### Generate a New Secret Key
```python
# Run in Python shell to generate a secure secret key:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Database Considerations
- **SQLite** works fine for small apps and development
- For production with more traffic, consider:
  - **PostgreSQL** (recommended for Railway/Heroku)
  - **MySQL**
  - Railway provides free PostgreSQL databases

### To Use PostgreSQL on Railway:
1. Add PostgreSQL service in Railway dashboard
2. Railway will provide `DATABASE_URL` environment variable
3. Update requirements.txt:
   ```
   psycopg2-binary==2.9.9
   dj-database-url==2.1.0
   ```
4. Update settings.py:
   ```python
   import dj_database_url
   
   if config('DATABASE_URL', default=None):
       DATABASES = {
           'default': dj_database_url.config(default=config('DATABASE_URL'))
       }
   ```

### Static Files
Whitenoise is already configured and will handle static files automatically on all platforms!

## Post-Deployment Checklist

After deploying:
1. ✅ Verify the app loads
2. ✅ Create a superuser: `railway run python manage.py createsuperuser`
3. ✅ Test login functionality
4. ✅ Check `/admin` works
5. ✅ Verify static files load correctly
6. ✅ Test API endpoints if you created any
7. ✅ Check logs for any errors

## Continuous Deployment

Railway (and most platforms) support automatic deployments:
- Push to GitHub main branch → Automatically deploys
- No manual steps needed after initial setup!

## Files Created for Deployment

- ✅ `Procfile` - Tells Railway/Heroku how to run the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `build.sh` - Build script for Render
- ✅ `requirements.txt` - Already exists
- ✅ `.gitignore` - Already exists
- ✅ `.env.example` - Template for environment variables

Your project is **ready to deploy** right now! 🚀
