### Getting Started

All containers can be started by running `docker-compose up` from the main directory.


### Database Migrations

```
# regular db
docker-compose exec server aerich init -t app.db.TORTOISE_ORM
docker-compose exec -e DATABASE_URL=$DATABASE_TEST_URL server aerich init-db

# test db
docker-compose exec -e DATABASE_URL=$DATABASE_TEST_URL server aerich init -t app.db.TORTOISE_ORM
docker-compose exec -e DATABASE_URL=$DATABASE_TEST_URL server aerich init-db
```
