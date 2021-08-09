# pull official base image
FROM python:3.9-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /app

# Add psql dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev geos gdal

# install dependencies
COPY ./requirements /app/requirements

RUN pip install --upgrade pip \
    && pip install -r ./requirements/dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/entrypoint.sh

# Give entrypoint permitions
RUN chmod +x /usr/src/entrypoint.sh
