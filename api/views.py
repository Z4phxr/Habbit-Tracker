from .serializers import HabitSerializer, SleepLogSerializer, MoodLogSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from base.models import MoodLog


@api_view(['POST'])
def mood_log_create(request):
    """
    Create or update mood log for a given day.
    Expects JSON: {"date": "YYYY-MM-DD", "mood": int}
    """
    date_str = request.data.get('date')
    mood = request.data.get('mood')
    if not date_str or mood is None:
        return Response({'error': 'Missing date or mood'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        mood_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    mood_log, created = MoodLog.objects.update_or_create(date=mood_date, defaults={'mood': mood})
    serializer = MoodLogSerializer(mood_log)
    return Response({'mood': mood_log.mood, 'created': created, 'id': mood_log.id}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def mood_log_delete_day(request):
    """
    Delete mood log for a given day.
    Expects ?date=YYYY-MM-DD in query params.
    """
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'Missing date'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        mood_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    deleted, _ = MoodLog.objects.filter(date=mood_date).delete()
    return Response({'deleted': deleted}, status=status.HTTP_200_OK)
from datetime import date, datetime, timedelta, time
import json

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Habit, HabitLog, SleepLog
from .serializers import HabitSerializer, SleepLogSerializer

# --- Habit endpoints ---

@api_view(['GET'])
def getData(request):
    """Return all habits."""
    habits = Habit.objects.all()
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addHabit(request):
    """Add a new habit."""
    serializer = HabitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteHabit(request, pk):
    """Delete a habit by primary key."""
    try:
        habit = Habit.objects.get(id=pk)
        habit.delete()
        return Response({'message': 'Habit deleted successfully'}, status=204)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=404)

@api_view(['PATCH'])
def updateHabit(request, pk):
    """Update habit name."""
    try:
        habit = Habit.objects.get(id=pk)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=404)
    new_name = request.data.get("name")
    if not new_name:
        return Response({'error': 'Name is required'}, status=400)
    habit.name = new_name
    habit.save()
    return Response({'message': 'Habit updated successfully'}, status=200)

@api_view(['PATCH'])
def toggle_archive(request, id):
    """Toggle habit archived status."""
    try:
        habit = Habit.objects.get(id=id)
    except Habit.DoesNotExist:
        return Response({"error": "Habit not found"}, status=404)
    habit.archived = not habit.archived
    habit.save()
    return Response({"archived": habit.archived}, status=200)

@api_view(['POST'])
def toggle_habit_log(request):
    """
    Toggle habit log for a given habit and date.
    If log exists, remove it. Otherwise, create it.
    """
    habit_id = request.data.get("habit_id")
    date_str = request.data.get("date")
    if not habit_id or not date_str:
        return Response({"error": "Missing habit_id or date"}, status=400)
    try:
        try:
            log_date = date.fromisoformat(date_str)
        except ValueError:
            log_date = datetime.strptime(date_str, "%B %d, %Y").date()
    except Exception as e:
        return Response({"error": f"Invalid date format: {e}"}, status=400)
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return Response({"error": "Habit not found"}, status=404)
    log, created = HabitLog.objects.get_or_create(habit=habit, date=log_date)
    if not created:
        log.delete()
        return Response({"message": "Log removed"}, status=204)
    else:
        log.completed = True
        log.save()
        return Response({"message": "Log created"}, status=201)

# --- SleepLog endpoints ---

@api_view(['GET', 'POST'])
def get_sleep_logs(request):
    """
    GET: Return all sleep logs (newest first).
    POST: Add a new sleep log.
    """
    if request.method == 'GET':
        sleep_logs = SleepLog.objects.all().order_by('-end')
        serializer = SleepLogSerializer(sleep_logs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SleepLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sleep_log_create(request):
    """
    Create a new sleep log. Always adds, does not replace.
    """
    data = json.loads(request.body)
    start = make_aware(datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S.%fZ"), get_current_timezone())
    end = make_aware(datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S.%fZ"), get_current_timezone())
    log = SleepLog.objects.create(start=start, end=end)
    duration = (end - start).total_seconds() / 3600
    return Response({'id': log.id, 'duration': duration}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def sleep_log_delete_day(request):
    """
    Delete all sleep logs for a given day.
    Expects ?date=YYYY-MM-DD in query params.
    """
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'Missing date'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)
    night_start = make_aware(datetime.combine(day - timedelta(days=1), time(20, 0)), get_current_timezone())
    night_end = night_start + timedelta(hours=16)
    deleted, _ = SleepLog.objects.filter(start__lt=night_end, end__gt=night_start).delete()
    return Response({'deleted': deleted}, status=status.HTTP_200_OK)

# --- Legacy/alternative sleep log save (not used by REST API) ---

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_sleep(request):
    """
    Save sleep log (used by non-REST API clients).
    Deletes previous logs for the same sleep period before saving.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        start = make_aware(parse_datetime(data["start"]))
        end = make_aware(parse_datetime(data["end"]))
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid input"}, status=400)
    sleep_date = end.date()
    night_start = make_aware(datetime.combine(sleep_date - timedelta(days=1), time(20, 0)))
    night_end = make_aware(datetime.combine(sleep_date, time(12, 0)))
    SleepLog.objects.filter(start__lt=night_end, end__gt=night_start).delete()
    new_log = SleepLog.objects.create(start=start, end=end)
    return JsonResponse({
        "id": new_log.id,
        "start": new_log.start.isoformat(),
        "end": new_log.end.isoformat(),
        "duration": str(new_log.duration),
        "sleep_date": str(new_log.sleep_date)
    })