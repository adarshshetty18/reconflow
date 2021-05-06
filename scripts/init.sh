#!/bin/bash
if [[ ! -e /reconflow/log ]]; then
    mkdir -p /reconflow/log
fi

if [[ ! -e /reconflow/conf ]]; then
    mkdir -p /reconflow/conf
fi

if [[ ! -e /reconflow/subdomains ]]; then
    mkdir -p /reconflow/subdomains
fi

if [[ ! -e /reconflow/livedomains ]]; then
    mkdir -p /reconflow/livedomains
fi

if [[ ! -e /reconflow/ports ]]; then
    mkdir -p /reconflow/ports
fi

if [[ ! -e /reconflow/directories ]]; then
    mkdir -p /reconflow/directories
fi

# Setting up Redis
MEM_TOTAL="$(grep 'MemTotal' /proc/meminfo | awk '{print $2}' |  xargs -I {} echo 'scale=0; {}*0.8/1024' | bc)"
MEM_TOTAL="${MEM_TOTAL}mb"
sed -i 's/# maxmemory <bytes>/maxmemory '"$MEM_TOTAL"'/g' /etc/redis/redis.conf
service redis-server start
export PATH=$PATH:/root/go/bin
source ~/.bashrc

figlet "Reconflow initiated successfully!"
supervisord -n