FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install pymysql
RUN pip install sqlmodel

# TODO: put all dependencies into requirements.txt and lock the versions

COPY ./app /app