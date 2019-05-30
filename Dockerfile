FROM python:3.7.3-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

