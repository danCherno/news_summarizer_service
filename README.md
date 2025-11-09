# Django News Aggregator API

A Django REST API that aggregates technology news and provides AI-powered summaries.

## Features

- 📰 Fetches tech articles from NewsAPI every 6 hours
- 🤖 AI summaries using ChatGPT (on-demand)
- 🔍 RESTful API with pagination
- 🐳 Dockerized deployment

## Quick Start

**1. Setup environment**

Create `.env` file:
```bash
NEWSAPI_KEY=your_key
OPENAI_API_KEY=your_key
SECRET_KEY=your_secret
DB_HOST=db
DB_NAME=devdb
DB_USER=devuser
DB_PASS=changeme
```

**2. Run with Docker**

```bash
docker-compose up --build
docker-compose run --rm app sh -c "python manage.py migrate"
```

**3. Access API**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## API Endpoints

```bash
GET  /api/articles/              # List articles (paginated)
GET  /api/articles/{id}/         # Get single article
GET  /api/articles/{id}/summary/ # Get/create AI summary
```

## Testing

```bash
docker-compose run --rm app sh -c "python manage.py test"
```

## Tech Stack

Django • DRF • PostgreSQL • OpenAI • Docker