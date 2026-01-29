"""
Web Authentication Views for Habit Tracker

Handles user login, registration, and logout for the web interface.
Uses Django's session authentication for web views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .utils import get_background


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Handle user login.
    
    GET: Display login form
    POST: Process login credentials
    """
    # If user is already logged in, redirect to habits
    if request.user.is_authenticated:
        return redirect('tracker', section='habits', period='week')
    
    background_image, button_gradient = get_background()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'auth/login.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
            })
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redirect to next page or default to habits tracker
            next_url = request.GET.get('next', '/track/habits/week/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html', {
        'background_image': background_image,
        'button_gradient': button_gradient,
    })


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    Handle user registration.
    
    GET: Display registration form
    POST: Process registration data
    """
    # If user is already logged in, redirect to habits
    if request.user.is_authenticated:
        return redirect('tracker', section='habits', period='week')
    
    background_image, button_gradient = get_background()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not username or not password or not email:
            messages.error(request, 'Username, email, and password are required.')
            return render(request, 'auth/register.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
                'username': username,
                'email': email,
            })
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
                'username': username,
                'email': email,
            })
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/register.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
                'username': username,
                'email': email,
            })
        
        # Check if email exists (required field)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/register.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
                'username': username,
                'email': email,
            })
        
        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'auth/register.html', {
                'background_image': background_image,
                'button_gradient': button_gradient,
                'username': username,
                'email': email,
            })
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Log the user in automatically after registration
        auth_login(request, user)
        messages.success(request, 'Account created successfully! Welcome to Habit Tracker.')
        return redirect('tracker', section='habits', period='week')
    
    return render(request, 'auth/register.html', {
        'background_image': background_image,
        'button_gradient': button_gradient,
    })


def logout_view(request):
    """
    Handle user logout.
    """
    auth_logout(request)
    return redirect('login')
