FROM python:3.7
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
ENV APP_ROOT /app
WORKDIR ${APP_ROOT}
RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
     apt-get clean
RUN pip install Django==3
COPY requirements.txt /${APP_ROOT}/requirements.txt
RUN pip install -r requirements.txt
COPY . ${APP_ROOT}
