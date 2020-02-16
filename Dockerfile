FROM python:3.8.1
MAINTAINER Valentin Hubert <valentin.hubert2@protonmail.com>

ENV PYTHONUNBUFFERED true

ENV JOB_LAUNCHER_DIRECTORY ./tmp

WORKDIR /app

CMD mkdir -p /app
CMD mkdir -p /app/test

COPY entrypoint.py /app/entrypoint.py
COPY script.sh /app/
COPY requirements.txt /app/

RUN chmod +x /app/entrypoint.py
RUN pip3 install -r /app/requirements.txt


ENTRYPOINT /app/entrypoint.py --folder /app/$JOB_LAUNCHER_DIRECTORY --script /app/script.sh
