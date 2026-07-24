.PHONY: help build test deploy-dev deploy-prod clean lint

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build:  ## Build Docker images locally
	docker-compose build

test:  ## Run unit tests
	pytest tests/ -v --cov=app --cov-report=term-missing

lint:  ## Run linters
	flake8 app/ --max-line-length=120
	black --check app/

format:  ## Auto-format code
	black app/
	isort app/

up:  ## Start services locally
	docker-compose up --build -d

down:  ## Stop services
	docker-compose down

deploy-dev:  ## Deploy to dev Kubernetes cluster
	helm upgrade --install microservices ./helm/myapp \
		--namespace dev --create-namespace \
		--set environment=dev \
		--wait

deploy-prod:  ## Deploy to production (requires confirmation)
	@echo "⚠️  Deploying to PRODUCTION. Press Ctrl+C to cancel..."
	@sleep 5
	helm upgrade --install microservices ./helm/myapp \
		--namespace production --create-namespace \
		--set environment=prod \
		--set replicaCount=3 \
		--wait --timeout 10m

rollout-status:  ## Check rollout status
	kubectl rollout status deployment/user-service -n dev
	kubectl rollout status deployment/product-service -n dev

logs:  ## View service logs
	kubectl logs -f deployment/user-service -n dev

clean:  ## Clean up resources
	docker-compose down --volumes --remove-orphans
	helm uninstall microservices -n dev || true
