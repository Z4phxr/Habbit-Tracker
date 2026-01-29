from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from base import views
from base import auth_views


def health_check(request):
    """Health check endpoint for monitoring and load balancers"""
    try:
        # Check database connection
        connection.ensure_connection()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
        }, status=503)


urlpatterns = [
    # Public pages
    path('', views.homepage, name='home'),
    path('health/', health_check, name='health'),
    
    # Authentication pages
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path("api/", include("api.urls")),
    
    # Protected pages (require login)
    path('track/<str:section>/<str:period>/', views.tracker, name='tracker'),
    path('track/edit/', views.edit_habits, name='edit_habits'),
]
