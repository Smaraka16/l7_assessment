.PHONY: build up down restart logs shell-backend shell-frontend migrate populate clean test-backend test-frontend test

# Build all containers
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Start all services with logs
up-logs:
	docker-compose up

# Stop all services
down:
	docker-compose down

# Restart all services
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# View backend logs
logs-backend:
	docker-compose logs -f backend

# View frontend logs
logs-frontend:
	docker-compose logs -f frontend

# Access backend shell
shell-backend:
	docker-compose exec backend bash

# Access frontend shell
shell-frontend:
	docker-compose exec frontend sh

# Run migrations
migrate:
	docker-compose exec backend python manage.py migrate

# Populate database
populate:
	docker-compose exec backend python manage.py movies

# Create superuser
superuser:
	docker-compose exec backend python manage.py createsuperuser

# Backend tests
test-backend:
	docker-compose exec backend pytest -v

# Frontend tests
test-frontend:
	cd frontend && npm test -- --run

# All tests
test:
	make test-backend && make test-frontend

# Clean everything (containers, volumes, images)
clean:
	docker-compose down -v
	docker system prune -f

# Rebuild and start
rebuild:
	docker-compose up --build -d

