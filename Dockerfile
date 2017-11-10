FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl && apt-get install -y bzip2 && apt-get install -y vim

RUN curl -LO https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -p /anaconda -b
RUN rm Anaconda3-5.0.1-Linux-x86_64.sh
ENV PATH=/anaconda/bin:$PATH
RUN mkdir /group_4_boilerplate
RUN pip install flask_wtf 
COPY group_4_boilerplate /group_4_boilerplate