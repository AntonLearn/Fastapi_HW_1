FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update
RUN apk add libpq-dev gcc python3-dev
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN chmod -R 777 ./