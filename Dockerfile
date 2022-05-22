FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update -y
RUN apt-get install git -y

COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT []
