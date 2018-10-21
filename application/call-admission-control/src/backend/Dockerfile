FROM python:2.7-stretch

RUN mkdir -p /app/src
COPY ./src /app/src
COPY ./run.py /app/
COPY ./wait-for-it.sh /app/
COPY ./docker-startup.sh /app/
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "docker-startup.sh"]
# RUN pwd
# CMD ["python", "run.py"]
