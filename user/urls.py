from django.urls import path, include
from . import views
from user.api.viewsets import (
    opaque_registration, 
    opaque_registration_finish,
    opaque_login,
    opaque_login_finish
)


urlpatterns = [
    # Template views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    
    # OPAQUE API endpoints
    path('o/registration', opaque_registration, name="o-reg"),
    path('o/registration/finish', opaque_registration_finish, name="o-reg-terminate"),
    path('o/login', opaque_login, name="o-login"),
    path('o/login/finish', opaque_login_finish, name="o-login-finish"),
]
