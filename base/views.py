from datetime import date, timedelta, datetime, time
import json
import calendar
from django.shortcuts import render
from django.utils.timezone import make_aware
from base.models import SleepLog, Habit, HabitLog, MoodLog
from .utils import get_background, return_motto

def homepage(request):
    background_image, button_gradient = get_background()
    return render(request, 'index.html', {
        'background_image': background_image,
        'button_gradient': button_gradient,
    })


def edit_habits(request):
    habits = Habit.objects.filter(archived=False)
    background_image, button_gradient = get_background()
    return render(request, "edit_habits.html", {
        'habits': habits,
        'background_image': background_image,
        'button_gradient': button_gradient,
    })

# Habits tracking views

def track_habits(request, view_mode='week'):
    background_image, button_gradient = get_background()
    habits = Habit.objects.filter(archived=False)

    # Get start date from GET params or use today
    start_date_str = request.GET.get('start_date')
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = date.today()
    else:
        start_date = date.today()

    if view_mode == 'day':
        days = [start_date]
        template_name = 'tracker_day.html'
        prev_start = start_date - timedelta(days=1)
        next_start = start_date + timedelta(days=1)
    elif view_mode == 'month':
        start_of_month = start_date.replace(day=1)
        _, last_day = calendar.monthrange(start_of_month.year, start_of_month.month)
        days = [start_of_month + timedelta(days=i) for i in range(last_day)]
        template_name = 'tracker_month.html'
        prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
        if start_of_month.month == 12:
            next_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1)
        else:
            next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
        prev_start = prev_month
        next_start = next_month
    else:  # week
        start_of_week = start_date - timedelta(days=start_date.weekday())
        days = [start_of_week + timedelta(days=i) for i in range(7)]
        template_name = 'tracker_week.html'
        prev_start = start_of_week - timedelta(days=7)
        next_start = start_of_week + timedelta(days=7)

    habit_logs = HabitLog.objects.filter(date__in=days, completed=True)
    log_dict = {f"{log.habit.id}-{log.date.isoformat()}": log.completed for log in habit_logs}

    context = {
        'habits': habits,
        'days': days,
        'background_image': background_image,
        'button_gradient': button_gradient,
        'active_view': view_mode,
        'motto': return_motto(),
        'log_dict_json': json.dumps(log_dict),
        'start_date': start_date,
        'prev_start': prev_start,
        'next_start': next_start,
        'active_section': 'habits',
        'active_period': view_mode,
    }

    return render(request, template_name, context)

# Sleep tracking views

def process_day(day: datetime):
    # Calculate the night period (20:00 previous day to 12:00 current day)
    night_start = make_aware(datetime.combine(day - timedelta(days=1), time(20, 0)))
    night_end = night_start + timedelta(hours=16)

    logs = SleepLog.objects.filter(start__lt=night_end, end__gt=night_start).order_by('-end')
    log = logs.first()  # Use only the newest log

    total_sleep = timedelta(0)
    if log:
        overlap_start = max(log.start, night_start)
        overlap_end = min(log.end, night_end)
        total_sleep += max(overlap_end - overlap_start, timedelta(0))

    hours = total_sleep.seconds // 3600
    minutes = (total_sleep.seconds % 3600) // 60
    sleep_time_str = f"{hours}h {minutes}min" if total_sleep else "–"

    # Split night into 16 hourly blocks and mark if slept
    blocks = []
    current = night_start
    for _ in range(16):
        block_end = current + timedelta(hours=1)
        slept = log and log.start < block_end and log.end > current
        blocks.append({
            "label": current.strftime("%H:%M"),
            "slept": slept
        })
        current = block_end

    hour_labels = [(night_start + timedelta(hours=i)).strftime("%H:%M") for i in range(17)]
    return blocks, sleep_time_str, hour_labels

def sleep_tracker(request):
    background_image, button_gradient = get_background()
    motto = "Track your sleep"

    date_str = request.GET.get("start_date")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        base_date = datetime.now().date()

    blocks, sleep_time_str, hour_labels = process_day(base_date)

    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'motto': motto,
        'blocks': blocks,
        'sleep_time_str': sleep_time_str,
        'hour_labels': hour_labels,
        'current_date': base_date.strftime("%d %b %Y"),
        'days': [base_date],  # Added for template date display
        'prev_start': (base_date - timedelta(days=1)),
        'next_start': (base_date + timedelta(days=1)),
        'active_section': 'sleep',
        'active_period': 'day',
    }

    return render(request, 'sleep_day.html', context)

def sleep_tracker_week(request):
    background_image, button_gradient = get_background()
    motto = "Track your sleep"

    date_str = request.GET.get("week")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        base_date = datetime.now().date()

    week_start = base_date - timedelta(days=base_date.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]
    week_blocks = []
    sleep_times = []

    # Aggregate sleep data for each day in the week
    for day in week_days:
        blocks, sleep_time, _ = process_day(day)
        week_blocks.append(blocks)
        sleep_times.append(sleep_time)

    hour_labels = [block["label"] for block in week_blocks[0]]
    zipped_days_blocks = list(zip(week_days, week_blocks, sleep_times))

    week_range_str = f"{week_start.strftime('%d %b')} – {(week_start + timedelta(days=6)).strftime('%d %b %Y')}"

    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'motto': motto,
        'zipped_days_blocks': zipped_days_blocks,
        'hour_labels': hour_labels,
        'days': week_days,  # Added for template week date display
        'prev_start': week_start - timedelta(days=7),
        'next_start': week_start + timedelta(days=7),
        'week_range': week_range_str,
        'active_section': 'sleep',
        'active_period': 'week',
    }

    return render(request, 'sleep_week.html', context)

def sleep_tracker_month(request):
    background_image, button_gradient = get_background()

    date_str = request.GET.get("month")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m").date()
    else:
        base_date = datetime.now().date()

    year = base_date.year
    month = base_date.month
    num_days = calendar.monthrange(year, month)[1]
    all_days = [date(year, month, day) for day in range(1, num_days + 1)]

    blocks_list = []
    sleep_times = []

    # Aggregate sleep data for each day in the month
    for day in all_days:
        blocks, sleep_time, _ = process_day(day)
        blocks_list.append(blocks)
        sleep_times.append(sleep_time)

    hour_labels = [block["label"] for block in blocks_list[0]]
    zipped_days_blocks = list(zip(all_days, blocks_list, sleep_times))

    prev_month = (base_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    next_month = (base_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'zipped_days_blocks': zipped_days_blocks,
        'hour_labels': hour_labels,
        'month_name': base_date.strftime("%B %Y"),
        'prev_month': prev_month.strftime("%Y-%m"),
        'next_month': next_month.strftime("%Y-%m"),
        'active_section': 'sleep',
        'active_period': 'month',
    }

    return render(request, 'sleep_month.html', context)

# Mood tracking views

def mood_tracker_day(request):
    background_image, button_gradient = get_background()
    date_str = request.GET.get("start_date")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        base_date = datetime.now().date()

    mood_log = MoodLog.objects.filter(date=base_date).first()
    mood_value = mood_log.mood if mood_log else None
    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'active_section': 'mood',
        'active_period': 'day',
        'current_date': base_date.strftime("%d %b %Y"),
        'day_obj': base_date,
        'prev_date': (base_date - timedelta(days=1)).strftime("%Y-%m-%d"),
        'next_date': (base_date + timedelta(days=1)).strftime("%Y-%m-%d"),
        'mood_log': mood_log,
        'mood_value': mood_value,
        'mood_range': range(1, 11),
    }
    return render(request, 'mood_day.html', context)

def mood_tracker_week(request):
    background_image, button_gradient = get_background()
    date_str = request.GET.get("week")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        base_date = datetime.now().date()

    week_start = base_date - timedelta(days=base_date.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]
    mood_logs = {log.date: log for log in MoodLog.objects.filter(date__in=week_days)}
    zipped_days_moods = [(day, mood_logs.get(day)) for day in week_days]

    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'active_section': 'mood',
        'active_period': 'week',
        'week_days': week_days,
        'zipped_days_moods': zipped_days_moods,
        'prev_week': (week_start - timedelta(days=7)).strftime("%Y-%m-%d"),
        'next_week': (week_start + timedelta(days=7)).strftime("%Y-%m-%d"),
        'week_range': f"{week_start.strftime('%d %b')} – {(week_start + timedelta(days=6)).strftime('%d %b %Y')}",
    }
    return render(request, 'mood_week.html', context)

def mood_tracker_month(request):
    background_image, button_gradient = get_background()
    date_str = request.GET.get("month")
    if date_str:
        base_date = datetime.strptime(date_str, "%Y-%m").date()
    else:
        base_date = datetime.now().date()

    year = base_date.year
    month = base_date.month
    num_days = calendar.monthrange(year, month)[1]
    all_days = [date(year, month, day) for day in range(1, num_days + 1)]
    mood_logs = {log.date: log for log in MoodLog.objects.filter(date__year=year, date__month=month)}
    zipped_days_moods = [(day, mood_logs.get(day)) for day in all_days]

    # Calculate empty slots before the first day of the month (Monday=0, Sunday=6)
    # For display, Monday is column 0, so weekday() is correct
    first_day_weekday = all_days[0].weekday()  # Monday=0, Sunday=6
    month_start_empty_slots = first_day_weekday

    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'active_section': 'mood',
        'active_period': 'month',
        'month_name': base_date.strftime("%B %Y"),
        'zipped_days_moods': zipped_days_moods,
        'prev_month': (base_date.replace(day=1) - timedelta(days=1)).strftime("%Y-%m"),
        'next_month': (base_date.replace(day=28) + timedelta(days=4)).strftime("%Y-%m"),
        'weekday_names': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'month_start_empty_slots': month_start_empty_slots,
    }
    return render(request, 'mood_month.html', context)

# Unified tracker view

def tracker(request, section, period):
    background_image, button_gradient = get_background()
    context = {
        'background_image': background_image,
        'button_gradient': button_gradient,
        'active_section': section,
        'active_period': period,
    }

    if section == 'habits':
        return track_habits(request, view_mode=period)
    elif section == 'sleep':
        if period == 'day':
            return sleep_tracker(request)
        elif period == 'week':
            return sleep_tracker_week(request)
        elif period == 'month':
            return sleep_tracker_month(request)
    elif section == 'mood':
        if period == 'day':
            return mood_tracker_day(request)
        elif period == 'week':
            return mood_tracker_week(request)
        elif period == 'month':
            return mood_tracker_month(request)

    return homepage(request)