FROM python:3.7.10-alpine3.12

RUN apk add --update --no-cache git make musl-dev go redis supervisor libpcap-dev

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH
RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin

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

ENTRYPOINT ["sh", "/opt/init.sh"]