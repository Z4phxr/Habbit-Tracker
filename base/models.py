from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"


class SleepLog(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    @property
    def duration(self):
        return self.end - self.start

    @property
    def sleep_date(self):
        return self.end.date()

    def __str__(self):
        return f"Sleep from {self.start} to {self.end} ({self.duration})"


class MoodLog(models.Model):
    date = models.DateField()
    mood = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)])
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date}: {self.mood}"
