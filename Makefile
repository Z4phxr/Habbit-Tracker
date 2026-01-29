.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services in detached mode
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs from all services
	docker-compose logs -f

logs-web: ## Show logs from web service
	docker-compose logs -f web

logs-db: ## Show logs from database service
	docker-compose logs -f db

shell: ## Open Django shell
	docker-compose exec web python manage.py shell

bash: ## Open bash shell in web container
	docker-compose exec web /bin/sh

migrate: ## Run database migrations
	docker-compose exec web python manage.py migrate

makemigrations: ## Create new migrations
	docker-compose exec web python manage.py makemigrations

createsuperuser: ## Create Django superuser
	docker-compose exec web python manage.py createsuperuser

collectstatic: ## Collect static files
	docker-compose exec web python manage.py collectstatic --noinput

test: ## Run tests
	docker-compose exec web python manage.py test

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --remove-orphans
	docker system prune -f

ps: ## Show running containers
	docker-compose ps

# Production targets
prod-build: ## Build production images
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

prod-up: ## Start production services
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

prod-logs: ## Show production logs
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Database backup
backup-db: ## Backup database
	docker-compose exec db pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Health check
health: ## Check service health
	@echo "Checking service health..."
	@curl -f http://localhost:8000/ && echo "Web service is healthy" || echo "Web service is not responding"
