FROM python:3.7.3-alpine
ADD . /code
WORKDIR /code
EXPOSE 5000
RUN pip3 install -r requirements.txt
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:5000" ]