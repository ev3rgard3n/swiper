FROM python:3.11.6

RUN mkdir /swiper

WORKDIR /swiper

COPY pyproject.toml .
COPY requirements.txt .

RUN pip install poetry
RUN poetry install

COPY . .

CMD gunicorn src.main:app --workers 1 --workers-class uvicorn.workers.UvicornWorkers --bind=0.0.0.0:8000