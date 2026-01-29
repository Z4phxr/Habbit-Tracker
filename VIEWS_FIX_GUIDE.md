# Quick Fix Script for base/views.py Syntax Errors

## The base/views.py file has syntax errors from incomplete edits.
## Here are the exact fixes needed:

### Issue 1: Missing closing parenthesis in process_day calls (appears twice)
**Location**: Lines ~202 and ~250

**Find**:
```python
blocks, sleep_time, _ = process_day(day, request.user
```

**Replace with**:
```python
blocks, sleep_time, _ = process_day(day, request.user)
```

### Issue 2: Missing return statement and closing brace
**Location**: Line ~177

**Find**:
```python
        'active_section': 'sleep',
        'active_period': 'day',
@login_required
```

**Replace with**:
```python
        'active_section': 'sleep',
        'active_period': 'day',
    }
    
    return render(request, 'sleep_day.html', context)

@login_required
```

### Issue 3: Missing return statement and closing brace
**Location**: Line ~223

**Find**:
```python
        'active_section': 'sleep',
        'active_period': 'week',
@login_required
```

**Replace with**:
```python
        'active_section': 'sleep',
        'active_period': 'week',
    }
    
    return render(request, 'sleep_week.html', context)

@login_required
```

### Issue 4: Missing return statement and closing brace  
**Location**: Line ~331

**Find**:
```python
        'prev_week': (week_start - timedelta(days=7)).strftime("%Y-%m-%d"),
        'next_week': (week_start + timedelta(days=7)).strftime("%Y-%m-%d"),
@login_required
```

**Replace with**:
```python
        'prev_week': (week_start - timedelta(days=7)).strftime("%Y-%m-%d"),
        'next_week': (week_start + timedelta(days=7)).strftime("%Y-%m-%d"),
        'week_range': f"{week_start.strftime('%d %b')} – {(week_start + timedelta(days=6)).strftime('%d %b %Y')}",
    }
    return render(request, 'mood_week.html', context)

@login_required
```

### Issue 5: Duplicate code section with incomplete filter
**Location**: Lines ~345-360

**Find** (the duplicate section):
```python
    mood_logs = {log.date: log for log in MoodLog.objects.filter(user=request.user, 
    month = base_date.month
    num_days = calendar.monthrange(year, month)[1]
    all_days = [date(year, month, day) for day in range(1, num_days + 1)]
    mood_logs = {log.date: log for log in MoodLog.objects.filter(date__year=year, date__month=month)}
```

**Replace with** (keep only the complete version):
```python
    mood_logs = {log.date: log for log in MoodLog.objects.filter(user=request.user, date__year=year, date__month=month)}
```

## After Manual Fixes, Run:
```bash
python -m py_compile base/views.py
python manage.py makemigrations
python manage.py migrate
```
