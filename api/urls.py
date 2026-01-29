from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Authentication URLs
    path('auth/register/', auth_views.register, name='api_register'),
    path('auth/login/', auth_views.login, name='api_login'),
    path('auth/logout/', auth_views.logout, name='api_logout'),
    path('auth/verify/', auth_views.verify_token, name='api_verify_token'),

    # Habit URLs
    path('habits/', views.getData, name="get_data"),
    path('habits/add_habit/', views.addHabit, name="add_habit"),
    path('habits/delete/<int:pk>/', views.deleteHabit, name="delete_habit"),
    path('habits/toggle/', views.toggle_habit_log, name="toggle_habit_log"),
    path('habits/update/<int:pk>/', views.updateHabit, name="update_habit"),
    path('habits/archive/<int:id>/', views.toggle_archive, name='toggle_archive'),

    # SleepLog URLs
    path('sleep/', views.get_sleep_logs, name="get_sleep_logs"),
    path('sleep/delete_day/', views.sleep_log_delete_day, name='sleep_log_delete_day'),

    # MoodLog URLs
    path('mood/', views.mood_log_create, name="mood_log_create"),
    path('mood/delete_day/', views.mood_log_delete_day, name="mood_log_delete_day"),
]