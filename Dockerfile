FROM python:3.7.3-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:5000 --chdir src 'app:app'