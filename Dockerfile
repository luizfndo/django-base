FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gettext \
    python3-gdal \
    postgresql-client

ADD . /django_base/

WORKDIR /django_base/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements_dev.txt

CMD ["/bin/bash", "-c", "while true; do sleep 10; done"]
