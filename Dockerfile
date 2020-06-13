FROM python:3.7.3-alpine
COPY ./mathlearning .
EXPOSE 5000
RUN pip3 install -r requirements.txt
CMD [ "python", "./manage.py", "runserver"]