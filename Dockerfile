FROM ubuntu:20.04

RUN echo "deb http://ap-south-1.ec2.archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list
RUN echo "deb-src http://ap-south-1.ec2.archive.ubuntu.com/ubuntu/ xenial main restricted" >> /etc/apt/sources.list
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libpcap-dev supervisor redis-server\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/reconflow
COPY core /usr/src/reconflow

# Installing go
RUN sudo wget https://golang.org/dl/go1.15.5.linux-amd64.tar.gz -P /usr/src/local/ && \
    tar -xzf /usr/src/local/go1.15.5.linux-amd64.tar.gz && \
    export PATH=$PATH:/usr/local/go/bin && \
    source ~/.bashrc

# Installing subfinder
RUN GO111MODULE=on go get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder

# Installing naabu
RUN GO111MODULE=on go get -v github.com/projectdiscovery/naabu/v2/cmd/naabu

# Installing httpx
RUN GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx

# Installing FFUF
RUN GO111MODULE=on go get -v github.com/ffuf/ffuf

ENTRYPOINT ["bash", "/opt/init.sh"]