FROM python:3-alpine

WORKDIR /usr/src/app/backend

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY requirements/ .
RUN pip install -r production.txt
COPY ./entrypoint.sh .
COPY ./start.sh .
RUN chmod +x entrypoint.sh
RUN mkdir media

COPY . .



ENTRYPOINT [ "/usr/src/app/backend/entrypoint.sh" ]

