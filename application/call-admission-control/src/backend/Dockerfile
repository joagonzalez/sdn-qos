FROM python:2.7-stretch

RUN mkdir -p /app/src
COPY ./src /app/src
COPY ./run.py /app/
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pwd
CMD ["python", "run.py"]
