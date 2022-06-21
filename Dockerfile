FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


RUN mkdir /code

WORKDIR /code

COPY . /code/
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]