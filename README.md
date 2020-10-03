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
