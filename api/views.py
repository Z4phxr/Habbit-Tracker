from .serializers import HabitSerializer, SleepLogSerializer, MoodLogSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from base.models import MoodLog


@api_view(['POST'])
def mood_log_create(request):
    """
    Create or update mood log for authenticated user for a given day.
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
    mood_log, created = MoodLog.objects.update_or_create(
        user=request.user,
        date=mood_date,
        defaults={'mood': mood}
    )
    serializer = MoodLogSerializer(mood_log)
    return Response({'mood': mood_log.mood, 'created': created, 'id': mood_log.id}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def mood_log_delete_day(request):
    """
    Delete mood log for authenticated user for a given day.
    Expects ?date=YYYY-MM-DD in query params.
    """
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'Missing date'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        mood_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    deleted, _ = MoodLog.objects.filter(user=request.user, date=mood_date).delete()
    return Response({'deleted': deleted}, status=status.HTTP_200_OK)
from datetime import date, datetime, timedelta, time
import json

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone
from django.utils import timezone as django_timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Habit, HabitLog, SleepLog
from .serializers import HabitSerializer, SleepLogSerializer

# --- Habit endpoints ---

@api_view(['GET'])
def getData(request):
    """Return all habits for authenticated user."""
    habits = Habit.objects.filter(user=request.user)
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addHabit(request):
    """Add a new habit for authenticated user."""
    serializer = HabitSerializer(data=request.data)
    if serializer.is_valid():
        # Associate habit with current user
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteHabit(request, pk):
    """Delete a habit by primary key (only if owned by user)."""
    try:
        habit = Habit.objects.get(id=pk, user=request.user)
        habit.delete()
        return Response({'message': 'Habit deleted successfully'}, status=204)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=404)

@api_view(['PATCH'])
def updateHabit(request, pk):
    """Update habit name (only if owned by user)."""
    try:
        habit = Habit.objects.get(id=pk, user=request.user)
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
    """Toggle habit archived status (only if owned by user)."""
    try:
        habit = Habit.objects.get(id=id, user=request.user)
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
    Only works with user's own habits.
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
        habit = Habit.objects.get(id=habit_id, user=request.user)
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
    GET: Return all sleep logs for authenticated user (newest first).
    POST: Add a new sleep log for authenticated user.
    """
    if request.method == 'GET':
        sleep_logs = SleepLog.objects.filter(user=request.user).order_by('-end')
        serializer = SleepLogSerializer(sleep_logs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SleepLogSerializer(data=request.data)
        if serializer.is_valid():
            # Associate sleep log with current user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sleep_log_create(request):
    """
    Create a new sleep log for authenticated user. Deletes previous log for the same night period.
    """
    data = json.loads(request.body)
    # Parse ISO datetime strings with Z suffix (UTC)
    start = parse_datetime(data['start'])
    end = parse_datetime(data['end'])
    
    # Delete any existing sleep logs that overlap with this night period
    # Determine which "night" this belongs to (based on end time - when you wake up)
    sleep_date = end.date()
    night_start = make_aware(datetime.combine(sleep_date - timedelta(days=1), time(18, 0)))
    night_end = night_start + timedelta(hours=24)
    
    # Delete overlapping logs for this user in this night period
    SleepLog.objects.filter(
        user=request.user,
        start__lt=night_end,
        end__gt=night_start
    ).delete()
    
    log = SleepLog.objects.create(user=request.user, start=start, end=end)
    duration = (end - start).total_seconds() / 3600
    return Response({'id': log.id, 'duration': duration}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def sleep_log_delete_day(request):
    """
    Delete all sleep logs for authenticated user for a given day.
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
    deleted, _ = SleepLog.objects.filter(
        user=request.user,
        start__lt=night_end,
        end__gt=night_start
    ).delete()
    return Response({'deleted': deleted}, status=status.HTTP_200_OK)

# --- Legacy/alternative sleep log save (not used by REST API) ---

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_sleep(request):
    """
    Save sleep log for authenticated user (used by non-REST API clients).
    Deletes previous logs for the same sleep period before saving.
    Note: This endpoint requires authentication but uses @csrf_exempt for legacy compatibility.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    
    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
        data = json.loads(request.body)
        start = make_aware(parse_datetime(data["start"]))
        end = make_aware(parse_datetime(data["end"]))
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid input"}, status=400)
    sleep_date = end.date()
    night_start = make_aware(datetime.combine(sleep_date - timedelta(days=1), time(20, 0)))
    night_end = make_aware(datetime.combine(sleep_date, time(12, 0)))
    SleepLog.objects.filter(
        user=request.user,
        start__lt=night_end,
        end__gt=night_start
    ).delete()
    new_log = SleepLog.objects.create(user=request.user, start=start, end=end)
    return JsonResponse({
        "id": new_log.id,
        "start": new_log.start.isoformat(),
        "end": new_log.end.isoformat(),
        "duration": str(new_log.duration),
        "sleep_date": str(new_log.sleep_date)
    })