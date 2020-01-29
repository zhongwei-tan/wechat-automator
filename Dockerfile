FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD python wechat.py && celery worker -l info --beat