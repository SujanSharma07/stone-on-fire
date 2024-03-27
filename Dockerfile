FROM python:3.9

LABEL maintainer="StreamesAlert"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ARG ENVIRONMENT=local

ENV USER app

USER root

ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y vim telnet build-essential curl libpq-dev --no-install-recommends \
    && mkdir -p /var/log/app /app /app/static /app/media

RUN python -m pip install --upgrade pip

WORKDIR /app/

COPY ./app/requirements.txt /tmp

RUN pip install pip-tools
RUN ln -sf /dev/stdout /var/log/app/uwsgi.log

RUN useradd -ms /bin/bash ${USER}
RUN pip3 install gunicorn==21.2.0
RUN pip3 install celery==5.3.5

USER ${USER}
RUN pip-sync /tmp/requirements.txt

COPY ./app .

CMD [ "gunicorn" , "config.wsgi:application" , "-b" , "0.0.0.0:20001" , "--workers" , "4", "--threads", "2", "--log-level" , "info"]

EXPOSE 20001