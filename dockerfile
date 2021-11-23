#FROM python:3.9-alpine
FROM python:slim
MAINTAINER Gergo Kurucz "gergo.kurucz@gmail.com"
#RUN apk update && apk add g++ make libffi-dev musl-dev
RUN apt-get update && apt-get install -y g++ make libffi-dev musl-dev && apt-get clean
#RUN git clone https://github.com/geer26/auth_server
#COPY . /app
RUN mkdir -p /counter
WORKDIR /counter
COPY requirements.txt /counter
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5001/tcp
#EXPOSE 3306/tcp
#EXPOSE 3306/udp
#ENTRYPOINT gunicorn -b 0.0.0.0:5001 -w 4 srv:app
ENTRYPOINT flask run

#docker build -t auth_server:latest .
#sudo docker run -d --net=host auth_server