FROM python:3.7.3-alpine
ADD ./mathlearning /code
WORKDIR /code
RUN pip3 install -r requirements.txt