FROM python:3.7-alpine
LABEL key="Michael Hixson"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./nosxihdsview01.pem /nosxihdsview01.pem
RUN apk add --update --no-cache postgresql-client libxml2-dev libxslt-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
