FROM python:3.7.3-alpine
ADD . /code
WORKDIR /code
EXPOSE 5000
RUN pip install -r requirements.txt