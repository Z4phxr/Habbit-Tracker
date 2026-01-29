from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from base import views


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
    path('', views.homepage, name='homepage'),
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path('track/<str:section>/<str:period>/', views.tracker, name='tracker'),
    path('track/edit/', views.edit_habits, name='edit_habits'),
]
