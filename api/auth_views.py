"""
Authentication Views for Habit Tracker API

This module provides secure authentication endpoints:
- User registration with validation
- Login with token generation
- Logout with token deletion
- Token verification

Using Django REST Framework's TokenAuthentication for security.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(['POST'])
@permission_classes([AllowAny])  # Public endpoint
def register(request):
    """
    Register a new user account.
    
    Expected JSON:
    {
        "username": "string",
        "email": "string (optional)",
        "password": "string"
    }
    
    Returns:
    - 201: User created successfully with auth token
    - 400: Validation errors
    """
    username = request.data.get('username')
    email = request.data.get('email', '')
    password = request.data.get('password')
    
    # Validate required fields
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if email already exists (if provided)
    if email and User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password strength using Django's built-in validators
    try:
        validate_password(password)
    except ValidationError as e:
        return Response(
            {'error': list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user with hashed password
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password  # Django automatically hashes this
    )
    
    # Generate authentication token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'message': 'User registered successfully',
        'token': token.key,
        'username': user.username,
        'user_id': user.id
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])  # Public endpoint
def login(request):
    """
    Login with username and password.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
    - 200: Login successful with auth token
    - 400: Missing credentials
    - 401: Invalid credentials
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user (checks password hash)
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create authentication token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'message': 'Login successful',
        'token': token.key,
        'username': user.username,
        'user_id': user.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requires valid token
def logout(request):
    """
    Logout by deleting the user's authentication token.
    
    Requires: Authorization header with token
    
    Returns:
    - 200: Logout successful
    """
    # Delete the user's token to invalidate it
    try:
        request.user.auth_token.delete()
    except AttributeError:
        # Token might not exist, that's ok
        pass
    
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requires valid token
def verify_token(request):
    """
    Verify that the current token is valid.
    
    Requires: Authorization header with token
    
    Returns:
    - 200: Token is valid with user info
    """
    return Response({
        'valid': True,
        'username': request.user.username,
        'user_id': request.user.id,
        'email': request.user.email
    }, status=status.HTTP_200_OK)
