FROM ubuntu:20.04

RUN echo "deb http://ap-south-1.ec2.archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list
RUN echo "deb-src http://ap-south-1.ec2.archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libpcap-dev supervisor redis-server wget software-properties-common \
  figlet bc vim ipython3\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

# Installing go
RUN add-apt-repository -y ppa:longsleep/golang-backports && \
    apt-get update && \
    apt-get install -y golang-go

# Installing subfinder
RUN GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder

# Installing naabu
RUN GO111MODULE=on go get -v github.com/projectdiscovery/naabu/v2/cmd/naabu

# Installing httpx
RUN GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx

# Installing FFUF
RUN GO111MODULE=on go get -v github.com/ffuf/ffuf

# Moving code
RUN mkdir -p /usr/src/reconflow
COPY core /usr/src/reconflow

# Copying scripts
ADD scripts/init.sh /opt/
ADD scripts/supervisord.conf /etc/supervisor/
ADD scripts/RF.conf /etc/supervisor/conf.d/

# Installing python dependencies
COPY scripts/requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

ENTRYPOINT ["bash", "/opt/init.sh"]