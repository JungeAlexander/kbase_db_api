FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./source/requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./source/db_api /app/db_api
