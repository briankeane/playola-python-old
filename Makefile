setup-database:
	docker-compose exec server aerich init -t app.db.TORTOISE_ORM
	docker-compose exec server aerich init-db

setup-test-database:
	docker-compose exec -e DATABASE_URL=$DATABASE_TEST_URL server aerich init -t app.db.TORTOISE_ORM
	docker-compose exec -e DATABASE_URL=$DATABASE_TEST_URL server aerich init-db
