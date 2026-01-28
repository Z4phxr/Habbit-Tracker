
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/


# Kopiuj entrypoint.sh jako tekstowy plik LF i wymuś chmod +x
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh || true
RUN chmod +x /entrypoint.sh

# Railway/Render: PORT z ENV
ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "habits_project.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
