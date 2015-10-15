# A dockerized IRC bot in python
# Version 0.1

FROM python:2.7.10
MAINTAINER Bren Briggs <briggs.brenton@gmail.com>

RUN apt-get update && apt-get install -y python-pip
RUN pip install selenium requests requests_ntlm
RUN mkdir -p /tipbot
COPY ./tipbot /tipbot/
CMD ["python","/tipbot/tipbot.py"]
