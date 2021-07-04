# FROM python:3.7.5
FROM python:3.7

WORKDIR /app/

ADD requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
