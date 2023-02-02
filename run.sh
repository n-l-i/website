#!/bin/bash

/bin/bash Deployment/init_website.sh $1 $2 $3 || exit 1
/bin/bash Deployment/host_website.sh $1 &
background_pid=$!
trap "kill $background_pid; pkill flask; exit 1" SIGEXIT SIGHUP SIGINT SIGTERM

while true; do
    sleep 300
    changes=$(git fetch && git rev-list HEAD...origin/main --count)
    if [ $changes -gt 0 ]; then
        kill $background_pid; pkill flask
        git pull
        /bin/bash Deployment/host_website.sh $1 &
        background_pid=$!
    fi
done
