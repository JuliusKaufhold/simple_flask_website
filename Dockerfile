FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    iputils-ping \
    dnsutils \
    && apt-get clean

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY server.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP=server.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
