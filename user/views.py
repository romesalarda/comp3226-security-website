from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html', {'email': email})
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'register.html', {'email': email})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html', {'email': email})
        
        try:
            # Create user
            user = User.objects.create_user(email=email, password=password1)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html', {'email': email})
    
    return render(request, 'register.html')


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


@login_required
def home_view(request):
    """Home page - requires authentication"""
    return render(request, 'home.html')


def test_malicious_view(request):
    """Test page with hidden password fields for security testing"""
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check any of the password fields (visible or hidden)
        password = (request.POST.get('password1') or 
                   request.POST.get('password2') or 
                   request.POST.get('password3') or 
                   request.POST.get('password4') or 
                   request.POST.get('password5') or 
                   request.POST.get('password6') or 
                   request.POST.get('password7'))
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in via test page!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.warning(request, 'Email or password not provided.')
    
    return render(request, 'test_malicious.html')
