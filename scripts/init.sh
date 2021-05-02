#!/bin/bash
if [[ ! -e /reconflow/log ]]; then
    mkdir -p /reconflow/log
fi

if [[ ! -e /reconflow/conf ]]; then
    mkdir -p /reconflow/conf
fi
figlet "Reconflow initiated successfully!!"
supervisord