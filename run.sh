#!/bin/bash

website_directory="$(realpath "$0" | xargs dirname)"
dev_mode=""
production_mode=""

print_usage_instructions() {
  echo "Error: Specify the required parameters of the available options."
  echo "       Available options:"
  echo "          -d: Select dev mode. Cannot be used in conjunction with -p."
  echo "          -p: Select production mode. Cannot be used in conjunction with -d."
}

while getopts ':dp' flag; do
  case "${flag}" in
    d) dev_mode='true' ;;
    p) production_mode='true' ;;
    *) print_usage_instructions; exit 1 ;;
  esac
done
[[ -z "$dev_mode" && -z "$production_mode" ]] && print_usage_instructions && exit 1
[[ ! -z "$dev_mode" && ! -z "$production_mode" ]] && print_usage_instructions && exit 1

(
    cd "$website_directory" && \
    source venv/bin/activate && \
    python3 -m Backend.fetch_repos
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd "$website_directory" && \
        source venv/bin/activate && \
        gunicorn --workers 4 \
                --bind 0.0.0.0:5001 \
                --certfile SSL_cert/fullchain.pem \
                --keyfile SSL_cert/privkey.pem \
                --ssl-version TLSv1_2 "Backend.server:get_app()"
    else
        cd "$website_directory" && \
        source venv/bin/activate && \
        flask run --host 0.0.0.0 \
                  --port 5001 \
                  --debugger
    fi
) &
wait
