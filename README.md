# DB API

```
docker build -t db_api:latest .
docker run -p 80:80 -e MAX_WORKERS="1" db_api:latest
```

## Setup

### Pre-commit

```
pre-commit install
```

## Notes

Full Stack FastAPI and PostgreSQL - Base Project Generator:
https://github.com/tiangolo/full-stack-fastapi-postgresql

## Testing

### Manually

#### PSQL

```
docker run --name kbase-db -v /Users/alexanderjunge/Code/kbase/db_api/data/pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpassword -p 10000:5432 -d postgres:13.0
psql -h localhost -p 10000 -U postgres
```
