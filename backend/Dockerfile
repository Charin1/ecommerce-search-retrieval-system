FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

# Models and index will be mounted via volumes in docker-compose
# but this ensures the directories exist.
RUN mkdir -p /app/models && mkdir -p /app/index && mkdir -p /app/data

EXPOSE 8000

# The command will be provided by docker-compose