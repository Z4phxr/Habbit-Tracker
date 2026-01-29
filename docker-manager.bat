@echo off
REM Habits Tracker - Docker Management Script for Windows
REM This script provides easy commands to manage your Docker application

:menu
cls
echo ========================================
echo   Habits Tracker - Docker Manager
echo ========================================
echo.
echo 1. Start Application
echo 2. Stop Application
echo 3. View Logs
echo 4. Restart Application
echo 5. Create Superuser
echo 6. Run Migrations
echo 7. Open Django Shell
echo 8. Backup Database
echo 9. Clean Up (Remove all containers and data)
echo 10. Check Status
echo 0. Exit
echo.
set /p choice="Enter your choice (0-10): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto superuser
if "%choice%"=="6" goto migrate
if "%choice%"=="7" goto shell
if "%choice%"=="8" goto backup
if "%choice%"=="9" goto clean
if "%choice%"=="10" goto status
if "%choice%"=="0" goto end
goto menu

:start
echo Starting application...
docker-compose up -d
echo.
echo Application started! Access at http://localhost:8000
pause
goto menu

:stop
echo Stopping application...
docker-compose down
echo Application stopped!
pause
goto menu

:logs
echo Showing logs (Press Ctrl+C to exit)...
docker-compose logs -f
pause
goto menu

:restart
echo Restarting application...
docker-compose restart
echo Application restarted!
pause
goto menu

:superuser
echo Creating superuser...
docker-compose exec web python manage.py createsuperuser
pause
goto menu

:migrate
echo Running migrations...
docker-compose exec web python manage.py migrate
echo Migrations complete!
pause
goto menu

:shell
echo Opening Django shell...
docker-compose exec web python manage.py shell
pause
goto menu

:backup
echo Creating database backup...
set timestamp=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
docker-compose exec -T db pg_dump -U postgres habits_db > backup_%timestamp%.sql
echo Backup created: backup_%timestamp%.sql
pause
goto menu

:clean
echo WARNING: This will remove all containers, volumes, and data!
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    docker-compose down -v --remove-orphans
    echo Cleanup complete!
) else (
    echo Cleanup cancelled.
)
pause
goto menu

:status
echo Checking application status...
docker-compose ps
echo.
echo Testing application health...
curl -f http://localhost:8000/health/ && echo. && echo Application is healthy! || echo. && echo Application is not responding!
pause
goto menu

:end
echo Goodbye!
exit /b
