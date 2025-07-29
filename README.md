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

## How to Open and Run the App

You can start the HABITS Tracker web app locally using the provided batch file or manually:

### Using the Batch File (Windows)
1. Ensure you have Python 3.13 and Django dependencies installed in your virtual environment (`venv`).
2. Double-click `Habbits.bat` or run it from the command line:
   ```bat
   Habbits.bat
   ```
   - This will activate your virtual environment, run migrations, start the Django server, and open the app in your default browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Manual Steps
1. Open a terminal in the project directory.
2. (If you don't have a virtual environment yet) Create one:
   ```bat
   python -m venv venv
   ```
3. Activate your virtual environment:
   ```bat
   .\venv\Scripts\activate
   ```
4. Install dependencies:
   ```bat
   pip install -r requirements.txt
   ```
   or, if using Pipfile:
   ```bat
   pip install pipenv
   pipenv install
   ```
5. Run migrations to set up the database:
   ```bat
   python manage.py migrate
   ```
6. Start the Django development server:
   ```bat
   python manage.py runserver
   ```
7. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000).


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
