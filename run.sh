#!/bin/bash

dev_mode=""
production_mode=""
mode_flag=""
website_url=""

print_usage_instructions() {
  echo "Error: Specify the required parameters of the available options."
  echo "       Available options:"
  echo "          -d or -p (required): Select either dev mode or production mode."
  echo "          -u value (required): Set the website URL."
}

while getopts ':dpu:' flag; do
  case "${flag}" in
    d) dev_mode="true"; mode_flag="-d" ;;
    p) production_mode="true"; mode_flag="-p" ;;
    u) website_url="${OPTARG}" ;;
    *) print_usage_instructions; exit 1 ;;
  esac
done
if [[ -z "$dev_mode" && -z "$production_mode" ]] ||
        [[ ! -z "$dev_mode" && ! -z "$production_mode" ]] ||
        [[ -z "$website_url" ]]; then
    print_usage_instructions
    exit 1
fi

/bin/bash Deployment/init_website.sh $mode_flag -u $website_url || exit 1
/bin/bash Deployment/host_website.sh $mode_flag &
background_pid=$!
if [[ "$mode_flag" == "-d" ]]; then
    trap "kill $background_pid; pkill flask; exit 1" EXIT HUP INT TERM
else
    trap "kill $background_pid; pkill gunicorn; exit 1" EXIT HUP INT TERM
fi

while true; do
    sleep 60
    changes=$(git fetch && git rev-list HEAD...origin/main --count)
    # If changes have been pushed to git origin or
    # if the flask/gunicorn server process has stopped
    if [[ $changes -gt 0 || -z "$(ps -A | grep 'flask\|gunicorn')" ]]; then
        kill $background_pid;
        if [[ "$mode_flag" == "-d" ]]; then
            pkill flask
        else
            pkill gunicorn
        fi
        git pull
        /bin/bash Deployment/host_website.sh $1 &
        background_pid=$!
    fi
done
