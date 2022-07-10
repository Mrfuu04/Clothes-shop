FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /docker_folder
COPY ./requirements.txt /docker_folder/requirements.txt
RUN apt-get update
RUN pip install -r requirements.txt
RUN apt-get install -y memcached
RUN apt-get install -y libmemcached-dev
COPY . /docker_folder/