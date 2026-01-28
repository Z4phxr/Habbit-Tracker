# HABITS Tracker

**Note: This project is a work in progress. Features and UI may change.**

A Django-based web application for tracking habits, sleep, and mood, with a modern, block-based visual interface and REST API support.

## Features

- **Habits Tracking**: Log daily, weekly, and monthly progress for custom habits. Visual tables show completion status.
- **Sleep Tracking**: Input sleep periods, view sleep blocks by day, week, and month. Color-coded blocks for easy visualization.
- **Mood Tracking**: Log daily mood (1-10 scale), view mood history in day, week, and month formats. Calendar-style month view with color-coded blocks.
- **REST API**: Endpoints for logging and deleting mood entries, supporting integration with other tools or mobile apps.
- **Custom Template Tags**: Dynamic color mapping for mood blocks using Django template filters.
- **Responsive UI**: Modern CSS layout, navigation, and visual feedback for all trackers.

## Technologies

- Python 3.13
- Django 5.2.3
- Django REST Framework
- SQLite (default, can be changed)
- HTML/CSS (custom templates)

## Usage

- Use the navigation menu to switch between Habits, Sleep, and Mood trackers.
- Click blocks to log or edit entries.
- Use arrows to navigate between days, weeks, and months.
- API endpoints are available under `/api/` for mood logging.

## Customization

- Add new habits via the edit habits page.
- Change background images and color schemes in `base/static/style.css` and `base/utils.py`.
- Extend API functionality in `api/views.py` and `api/serializers.py`.


## Jak uruchomić lokalnie przez Docker

1. Skopiuj plik `.env.example` do `.env` i uzupełnij wartości (np. SECRET_KEY).
2. Zbuduj i uruchom kontenery:
   ```sh
   docker-compose up --build
   ```
3. Aplikacja będzie dostępna na [http://localhost:8000](http://localhost:8000)
4. Aby zatrzymać i usunąć kontenery:
   ```sh
   docker-compose down
   ```

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
