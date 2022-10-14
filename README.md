# Diskuze API FastAPI

Solution to IT Academy project

## First starting the project

Setup the environment

```sh
poetry install
poetry shell
```

Run local server

```sh
uvicorn diskuze:app --reload
```

Open GraphiQL on address http://127.0.0.1:5000/graphql and run the test query

```graphql
{
  hello
  total
}
```

## Extras

### Running database locally

```sh
docker-compose up database
mysql -uroot -proot -h127.0.0.1 diskuze < utils/db/db.sql
mysql -uroot -proot -h127.0.0.1 diskuze < utils/db/discussion.sql
mysql -uroot -proot -h127.0.0.1 diskuze < utils/db/user.sql
mysql -uroot -proot -h127.0.0.1 diskuze < utils/db/comment.sql
```

### Running performance tests

```sh
wrk -s utils/wrk/request.lua --timeout 5 --latency http://127.0.0.1:8000/graphql
```
