from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from base.models import Habit, HabitLog, SleepLog, MoodLog
from datetime import date, datetime, timedelta


class HabitAPITestCase(TestCase):
    """Test API endpoints for habits with authentication."""
    
    def setUp(self):
        """Create test user and authenticate."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_add_habit_authenticated(self):
        """Test adding a habit with authentication."""
        response = self.client.post('/api/habits/add_habit/', {'name': 'Exercise'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.name, 'Exercise')
        self.assertEqual(habit.user, self.user)
    
    def test_add_habit_missing_user(self):
        """Test that habit serializer handles user assignment."""
        response = self.client.post('/api/habits/add_habit/', {'name': 'Read'}, format='json')
        self.assertEqual(response.status_code, 201)
        habit = Habit.objects.first()
        self.assertIsNotNone(habit.user)
    
    def test_add_habit_unauthenticated(self):
        """Test adding habit without authentication fails."""
        self.client.credentials()  # Remove authentication
        response = self.client.post('/api/habits/add_habit/', {'name': 'Exercise'}, format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_get_habits_authenticated(self):
        """Test getting habits for authenticated user."""
        Habit.objects.create(name='Exercise', user=self.user)
        Habit.objects.create(name='Read', user=self.user)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_get_habits_only_own(self):
        """Test that users only see their own habits."""
        other_user = User.objects.create_user(username='other', password='pass')
        Habit.objects.create(name='My Habit', user=self.user)
        Habit.objects.create(name='Other Habit', user=other_user)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'My Habit')
    
    def test_delete_habit(self):
        """Test deleting a habit."""
        habit = Habit.objects.create(name='Exercise', user=self.user)
        response = self.client.delete(f'/api/habits/delete/{habit.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)
    
    def test_delete_habit_not_owned(self):
        """Test cannot delete other user's habit."""
        other_user = User.objects.create_user(username='other', password='pass')
        habit = Habit.objects.create(name='Exercise', user=other_user)
        response = self.client.delete(f'/api/habits/delete/{habit.id}/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Habit.objects.count(), 1)
    
    def test_update_habit(self):
        """Test updating habit name."""
        habit = Habit.objects.create(name='Exercise', user=self.user)
        response = self.client.patch(
            f'/api/habits/update/{habit.id}/',
            {'name': 'Morning Exercise'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertEqual(habit.name, 'Morning Exercise')
    
    def test_toggle_archive(self):
        """Test archiving/unarchiving habit."""
        habit = Habit.objects.create(name='Exercise', user=self.user)
        response = self.client.patch(f'/api/habits/archive/{habit.id}/')
        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertTrue(habit.archived)
        
        # Toggle again
        response = self.client.patch(f'/api/habits/archive/{habit.id}/')
        habit.refresh_from_db()
        self.assertFalse(habit.archived)
    
    def test_toggle_habit_log(self):
        """Test toggling habit completion log."""
        habit = Habit.objects.create(name='Exercise', user=self.user)
        today = date.today().isoformat()
        
        # Create log
        response = self.client.post(
            '/api/habits/toggle/',
            {'habit_id': habit.id, 'date': today},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(HabitLog.objects.count(), 1)
        
        # Remove log
        response = self.client.post(
            '/api/habits/toggle/',
            {'habit_id': habit.id, 'date': today},
            format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(HabitLog.objects.count(), 0)


class SleepLogAPITestCase(TestCase):
    """Test API endpoints for sleep logs."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_create_sleep_log(self):
        """Test creating a sleep log."""
        from django.utils.timezone import make_aware
        start = make_aware(datetime.now() - timedelta(hours=8))
        end = make_aware(datetime.now())
        response = self.client.post(
            '/api/sleep/',
            {
                'start': start.isoformat(),
                'end': end.isoformat()
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SleepLog.objects.count(), 1)
    
    def test_get_sleep_logs(self):
        """Test getting sleep logs."""
        from django.utils.timezone import make_aware
        SleepLog.objects.create(
            user=self.user,
            start=make_aware(datetime.now() - timedelta(hours=8)),
            end=make_aware(datetime.now())
        )
        response = self.client.get('/api/sleep/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class MoodLogAPITestCase(TestCase):
    """Test API endpoints for mood logs."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_create_mood_log(self):
        """Test creating a mood log."""
        today = date.today().isoformat()
        response = self.client.post(
            '/api/mood/',
            {'date': today, 'mood': 5},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MoodLog.objects.count(), 1)
    
    def test_update_mood_log(self):
        """Test updating existing mood log."""
        today = date.today().isoformat()
        # Create
        self.client.post('/api/mood/', {'date': today, 'mood': 5}, format='json')
        # Update
        response = self.client.post('/api/mood/', {'date': today, 'mood': 8}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MoodLog.objects.count(), 1)
        self.assertEqual(MoodLog.objects.first().mood, 8)


class WebAuthTestCase(TestCase):
    """Test web authentication views."""
    
    def setUp(self):
        self.client = Client()
    
    def test_register_new_user(self):
        """Test user registration."""
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!'
        })
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_logout(self):
        """Test logout."""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

