FROM python:3.10-alpine

RUN adduser -D statistics

WORKDIR /home/statistics

COPY dist/person-statistics-0.1.0.tar.gz person-statistics-0.1.0.tar.gz
COPY docker-files/* ./
RUN python -m venv venv

RUN apk update && apk add --virtual build-dependencies gcc libc-dev make libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "venv/bin/pip install person-statistics-0.1.0.tar.gz"
RUN apk del build-dependencies
RUN venv/bin/pip install gunicorn

RUN mkdir data
RUN chown -R statistics:statistics ./
USER statistics

RUN chmod +x boot-web.sh

ENTRYPOINT ["./boot-web.sh"]