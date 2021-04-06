# DB API

```
docker build -t db_api:latest .
docker run -p 80:80 -e MAX_WORKERS="1" db_api:latest
```

## Setup

### Poetry

```
poetry install --no-root
jupyter nbextension enable --py widgetsnbextension
```

### Pre-commit

```
pre-commit install
```

## Notes

Full Stack FastAPI and PostgreSQL - Base Project Generator:
https://github.com/tiangolo/full-stack-fastapi-postgresql

## Testing

### Manually

### Pytest

```
poetry run pytest -v tests
```

#### PostgreSQL

```
docker kill $(docker ps -a -q)
docker rm $(docker ps -a -q)
rm -rf data/pgdata

docker run --name kbase-db -v /Users/alexanderjunge/Code/kbase/db_api/data/pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=password -p 10000:5432 -d postgres:13.0
psql -h localhost -p 10000 -U postgres
```

Initialize database:

```
poetry run alembic upgrade head
```

Setup initial superuser:

```
cd source
export PYTHONPATH=`pwd`:${PYTHONPATH}
poetry run python db_api/init_data.py
```

And further users for apps etc by running `notebooks/20200106_machine_tokens.ipynb`.

#### FastAPI

```
cd source/
poetry run uvicorn db_api.main:app --reload
```

Or:

```
export PYTHONPATH=`pwd`:$PYTHONPATH
poetry run python db_api/main.py
```
