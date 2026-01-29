from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    # Link each habit to a user - each user has their own habits
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        # Ensure habits are ordered by creation date
        ordering = ['created_at']
        # Add index for faster queries
        indexes = [
            models.Index(fields=['user', 'archived']),
        ]

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    class Meta:
        # Ensure unique logs per habit per day
        unique_together = ['habit', 'date']
        indexes = [
            models.Index(fields=['habit', 'date']),
        ]

    def __str__(self):
        return f"{self.habit.name} - {self.date}"


class SleepLog(models.Model):
    # Each sleep log belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_logs')
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ['-end']
        indexes = [
            models.Index(fields=['user', 'start', 'end']),
        ]

    @property
    def duration(self):
        return self.end - self.start

    @property
    def sleep_date(self):
        return self.end.date()

    def __str__(self):
        return f"Sleep from {self.start} to {self.end} ({self.duration})"


class MoodLog(models.Model):
    # Each mood log belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    date = models.DateField()
    mood = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)])
    note = models.TextField(blank=True)

    class Meta:
        # Ensure unique mood per user per day
        unique_together = ['user', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.date}: {self.mood}"
