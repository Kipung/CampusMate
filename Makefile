dev:
	docker-compose up -d --build

test:
	docker-compose exec backend pytest test_main.py
	docker-compose run --rm frontend npm test -- --watchAll=false

lint:
	docker-compose exec backend ruff check --fix .
	cd frontend && npm run format
	cd frontend && ./node_modules/.bin/eslint --fix src/
