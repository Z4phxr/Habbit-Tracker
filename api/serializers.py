from rest_framework import serializers
from base.models import Habit, SleepLog
from base.models import MoodLog

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

class SleepLogSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)
    sleep_date = serializers.DateField(read_only=True)

    class Meta:
        model = SleepLog
        fields = ['id', 'start', 'end', 'duration', 'sleep_date']


class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ['id', 'date', 'mood', 'note']