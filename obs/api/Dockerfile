FROM python:3.9-alpine

RUN mkdir /app
WORKDIR /app
COPY obs/api/requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt \
    && pip3 install gunicorn 
EXPOSE 5000

COPY . /app
WORKDIR /app/obs/api
