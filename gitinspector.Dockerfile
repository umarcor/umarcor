FROM python:3.7-alpine

RUN apk update && apk add git

RUN cd /opt \
 && git clone https://github.com/ejwa/gitinspector \
 && cd gitinspector \
 && pip install .
