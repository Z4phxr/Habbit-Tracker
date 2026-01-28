# Habits Tracker

**A Django-based web application for tracking habits, sleep, and mood with a modern visual interface and REST API support.**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-5.2.3-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)

## ✨ Features

- **📊 Habits Tracking**: Log daily, weekly, and monthly progress for custom habits with visual completion status
- **😴 Sleep Tracking**: Input sleep periods with color-coded blocks for easy visualization across day/week/month views
- **😊 Mood Tracking**: Log daily mood (1-10 scale) with calendar-style views and color-coded indicators
- **🔌 REST API**: Complete API endpoints for integration with other tools and mobile apps
- **🐳 Docker Ready**: Fully containerized with production-ready configuration
- **🚀 Easy Deployment**: One-command deployment to any cloud platform
- **🔒 Production Ready**: Security best practices, health checks, and monitoring built-in

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Habbit-Tracker

# 2. Copy environment file and configure
cp .env.example .env
# Edit .env with your settings

# 3. Start the application
docker-compose up -d

# 4. Access at http://localhost:8000
```

**That's it!** The application is now running with PostgreSQL.

For detailed instructions, see [QUICKSTART.md](QUICKSTART.md)

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide with platform-specific instructions
- **[Makefile](Makefile)** - Common commands and tasks

## 🛠️ Technologies

- **Backend**: Python 3.11, Django 5.2.3
- **Database**: PostgreSQL 15 (SQLite for development)
- **API**: Django REST Framework
- **Server**: Gunicorn with multiple workers
- **Proxy**: Nginx (optional, for production)
- **Container**: Docker & Docker Compose
- **Static Files**: WhiteNoise for efficient serving

## 📋 Common Commands

Using Make (recommended):

```bash
make up                 # Start all services
make down              # Stop all services
make logs              # View logs
make shell             # Open Django shell
make migrate           # Run database migrations
make createsuperuser   # Create admin user
make test              # Run tests
make backup-db         # Backup database
```

Using Docker Compose directly:

```bash
docker-compose up -d              # Start services
docker-compose logs -f            # View logs
docker-compose exec web bash     # Open shell
docker-compose down              # Stop services
```

## 🏗️ Project Structure

```
Habbit-Tracker/
├── 📁 base/              # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── static/           # CSS, images
│   └── templates/        # HTML templates
├── 📁 api/               # REST API
│   ├── views.py          # API endpoints
│   └── serializers.py    # Data serialization
├── 📁 habits_project/    # Django project settings
│   └── settings.py       # Configuration
├── 🐳 Dockerfile         # Multi-stage production image
├── 🐳 docker-compose.yml # Development setup
├── 📝 requirements.txt   # Python dependencies
├── 🔧 .env.example       # Environment template
└── 📚 DEPLOYMENT.md      # Deployment guide
```

## 🌐 Deployment

This application is ready to deploy to:

- **AWS EC2** / **Lightsail**
- **DigitalOcean Droplets**
- **Azure Container Instances**
- **Google Cloud Run**
- **Heroku**
- **Railway**
- **Render**
- Any VPS with Docker support

See [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific guides.

## 🔒 Security Features

- ✅ Multi-stage Docker build with minimal attack surface
- ✅ Non-root container user
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ HTTPS support with SSL redirect
- ✅ Secure cookie configuration
- ✅ Environment-based secrets management
- ✅ Database connection pooling
- ✅ Health checks and monitoring

## 🎯 Usage

- Use the navigation menu to switch between Habits, Sleep, and Mood trackers
- Click blocks to log or edit entries
- Use arrows to navigate between days, weeks, and months
- API endpoints available at `/api/` for programmatic access
- Admin panel at `/admin` for management

## 🔧 Customization

- **Add new habits**: Via the edit habits page
- **Styling**: Modify `base/static/style.css`
- **Colors**: Update color schemes in `base/utils.py`
- **API**: Extend functionality in `api/views.py`
- **Settings**: Configure in `habits_project/settings.py` or via environment variables

## 📊 API Endpoints

```
GET  /api/mood/          # List mood entries
POST /api/mood/          # Create mood entry
GET  /api/mood/{id}/     # Get specific entry
PUT  /api/mood/{id}/     # Update entry
DELETE /api/mood/{id}/   # Delete entry
```

## 🐛 Troubleshooting

If you encounter issues:

1. **Check logs**: `docker-compose logs -f`
2. **Verify .env**: Ensure all required variables are set
3. **Database issues**: Check PostgreSQL is running `docker-compose ps`
4. **Port conflicts**: Change PORT in .env if 8000 is taken
5. **See detailed troubleshooting**: [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for excellent documentation
- Docker for containerization platform
- PostgreSQL for robust database

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
