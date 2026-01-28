# Habit Tracker

> A simple web application for tracking daily habits, sleep patterns, and mood with visual progress indicators.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-5.2.3-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

## 📖 About

Habit Tracker helps you monitor your daily habits, sleep quality, and mood over time. View your progress in day, week, or month formats with intuitive color-coded visual blocks.

## ✨ Features

- 📊 **Habit Tracking** - Create custom habits and track daily completion
- 😴 **Sleep Logging** - Record sleep periods and visualize patterns
- 😊 **Mood Tracking** - Log daily mood on a 1-10 scale
- 📅 **Multiple Views** - See data by day, week, or month
- 🎨 **Visual Interface** - Color-coded blocks for easy progress monitoring
- 🔌 **REST API** - Integrate with other tools

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose installed

### Run the Application

```bash
# Clone the repository
git clone <your-repo-url>
cd Habbit-Tracker

# Copy and configure environment file
cp .env.example .env

# Start the application
docker-compose up -d

# Access the app at http://localhost:8000
```

That's it! Your habit tracker is now running.

## 🛠️ Built With

- **Backend**: Python 3.11, Django 5.2.3
- **Database**: PostgreSQL 15 (SQLite for development)

- **Backend**: Django 5.2.3, Python 3.11
- **Database**: PostgreSQL 15
- **Frontend**: HTML, CSS, JavaScript
- **Server**: Gunicorn
- **Containerization**: Docker & Docker Compose

## 📝 Usage

### Navigate the App

1. **Home Page** - Overview of all tracking sections
2. **Habits** - Create and track custom habits
3. **Sleep** - Log sleep periods and view patterns
4. **Mood** - Record daily mood ratings
5. **Edit** - Manage your habit list

### Common Commands

```bash
# View logs
docker-compose logs -f

# Stop the app
docker-compose down

# Restart
docker-compose restart

# Create admin user
docker-compose exec web python manage.py createsuperuser
```

### Windows Users

Double-click `docker-manager.bat` for an easy-to-use menu interface!

## 📊 API Endpoints

```
GET  /api/mood/          # List mood entries
POST /api/mood/          # Create mood entry
GET  /api/mood/{id}/     # Get specific entry
PUT  /api/mood/{id}/     # Update entry
DELETE /api/mood/{id}/   # Delete entry
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

Built with Django, PostgreSQL, and Docker.

## Jak zdeployować na Railway/Render

1. Wgraj cały projekt do repozytorium GitHub.
2. Skonfiguruj Railway/Render:
   - Ustaw zmienne środowiskowe z `.env.example` (szczególnie SECRET_KEY, DB, PORT)
   - Wskaż komendę startową:
     ```sh
     gunicorn habits_project.wsgi:application --bind 0.0.0.0:${PORT}
     ```
   - Railway/Render automatycznie wykryje PORT z ENV
3. Dodaj bazę danych PostgreSQL przez panel Railway/Render i uzupełnij zmienne w projekcie.
4. Deploy nastąpi automatycznie po każdym pushu do repozytorium.

## Pliki konfiguracyjne i ich rola

- `Dockerfile` – buduje obraz produkcyjny Django z Gunicornem, obsługuje zmienne środowiskowe, pliki statyczne.
- `docker-compose.yml` – uruchamia aplikację i bazę PostgreSQL, mapuje porty, korzysta z pliku `.env`.
- `.env.example` – przykładowe zmienne środowiskowe (skopiuj do `.env` do uruchomienia lokalnie).
- `entrypoint.sh` – skrypt startowy: migracje, collectstatic, uruchomienie Gunicorna.
- `.github/workflows/docker-build.yml` – workflow GitHub Actions: buduje i opcjonalnie publikuje obraz Dockera do GHCR.
- `.github/workflows/ci.yml` – workflow GitHub Actions: testy, lint, migracje na PR/main.
- `habits_project/settings.py` – obsługa produkcyjnych zmiennych środowiskowych, STATIC_ROOT, MEDIA_ROOT, ALLOWED_HOSTS, PORT.

## Checklist: uruchomienie lokalne przez Docker

- [ ] Skopiuj `.env.example` do `.env` i ustaw wartości
- [ ] `docker-compose up --build`
- [ ] Sprawdź logi: `docker-compose logs web`
- [ ] Aplikacja działa na [http://localhost:8000](http://localhost:8000)

## Checklist: deploy na Railway/Render

- [ ] Wgraj repozytorium na GitHub
- [ ] Skonfiguruj zmienne środowiskowe w panelu
- [ ] Dodaj bazę PostgreSQL przez panel
- [ ] Ustaw komendę startową Gunicorn
- [ ] Deploy automatyczny po pushu


## Planned Features

The following improvements and new features are planned for future releases:

- **Statistics Dashboard**: Visual summaries and charts for habits, sleep, and mood trends over time.
- **Direct Day Navigation**: Click on a day in week/month views to jump directly to the detailed day view.
- **Advanced Filtering**: Filter habits, sleep, and mood logs by tags, categories, or custom time ranges.
- **Mobile-Friendly UI**: Enhanced mobile layout and touch interactions for easier use on phones and tablets.
- **Export/Import Data**: Download your logs as CSV/Excel or import data from other sources.
- **User Accounts**: Multi-user support with authentication and personalized data.
- **Dark Mode**: Optional dark theme for better night-time usability.
- **Customizable Color Schemes**: User-selectable themes and color palettes for blocks and backgrounds.
- **Habit Streaks & Achievements**: Visual indicators for streaks and motivational badges.
- **Notes & Comments**: Add notes or comments to any log entry for more context.

If you have suggestions or feature requests, feel free to open an issue or contribute!

## License

MIT License
