FROM ubuntu:latest

# use aptitute to get packages for pulling and installing conda and vim for editing 
RUN apt-get update && apt-get install -y curl && apt-get install -y bzip2 && apt-get install -y vim

# get and install miniconda configure environment var
RUN curl -LO https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /anaconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/anaconda/bin:$PATH

# get flask_wtf for forms
RUN pip install flask_wtf 

# copy over source code
RUN mkdir /web_app && mkdir /web_app/static && mkdir /web_app/templates
COPY group_4_boilerplate/app.py /web_app
COPY group_4_boilerplate/forms.py /web_app
COPY group_4_boilerplate/make_database.py /web_app
COPY group_4_boilerplate/refugee.py /web_app
COPY group_4_boilerplate/config.py /web_app
COPY group_4_boilerplate/static /web_app/static/
COPY group_4_boilerplate/templates /web_app/templates/