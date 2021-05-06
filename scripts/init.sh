#!/bin/bash
if [[ ! -e /reconflow/log ]]; then
    mkdir -p /reconflow/log
fi

if [[ ! -e /reconflow/conf ]]; then
    mkdir -p /reconflow/conf
fi

# Setting up Redis
MEM_TOTAL="$(grep 'MemTotal' /proc/meminfo | awk '{print $2}' |  xargs -I {} echo 'scale=0; {}*0.8/1024' | bc)"
MEM_TOTAL="${MEM_TOTAL}mb"
sed -i 's/# maxmemory <bytes>/maxmemory '"$MEM_TOTAL"'/g' /etc/redis/redis.conf
service redis-server start

figlet "Reconflow initiated successfully!"
supervisord -n