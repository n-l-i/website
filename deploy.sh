#!/bin/bash

/bin/bash init.sh $1 $2 $3
/bin/bash run.sh $1 &
background_pid=$!
trap "kill $background_pid; exit 1" SIGEXIT SIGHUP SIGINT SIGTERM

while true; do
    sleep 300
    changes=$(git fetch && git rev-list HEAD...origin/main --count)
    if [ $changes -gt 0 ]; then
        kill $background_pid
        git pull
        /bin/bash run.sh $1 &
        background_pid=$!
    fi
done
