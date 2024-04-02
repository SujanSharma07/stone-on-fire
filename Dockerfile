FROM python:3.9

LABEL maintainer="sujansharma202@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ARG ENVIRONMENT=local

ENV USER app

USER root

ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y vim telnet build-essential curl libpq-dev --no-install-recommends \
    && mkdir -p /var/log/app /app /app/static /app/media

RUN python -m pip install --upgrade pip

WORKDIR /app/
COPY ./application/requirements.txt /tmp

RUN pip install pip-tools
RUN ln -sf /dev/stdout /var/log/app/uwsgi.log

RUN pip3 install -r /tmp/requirements.txt
RUN useradd -ms /bin/bash ${USER}
RUN pip3 install gunicorn==21.2.0


COPY ./application .

# RUN python3 manage.py collectstatic

# USER ${USER}

CMD [ "gunicorn" , "config.wsgi:application" , "-b" , "0.0.0.0:20001" , "--workers" , "4", "--threads", "2", "--log-level" , "info"]

EXPOSE 20001
