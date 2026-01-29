from rest_framework import serializers
from base.models import Habit, SleepLog
from base.models import MoodLog

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']

class SleepLogSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        start = validated_data['start']
        end = validated_data['end']
        from datetime import timedelta
        if 19 <= start.hour <= 23:
            start = start - timedelta(days=1)
            end = end - timedelta(days=1)
        validated_data['start'] = start
        validated_data['end'] = end
        return super().create(validated_data)
    duration = serializers.DurationField(read_only=True)
    sleep_date = serializers.DateField(read_only=True)

    class Meta:
        model = SleepLog
        fields = ['id', 'start', 'end', 'duration', 'sleep_date']
        read_only_fields = ['user']


class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ['id', 'date', 'mood', 'note']
        read_only_fields = ['user']