#!/bin/bash

website_directory="$(realpath "$0" | xargs dirname)/.."
dev_mode=""
production_mode=""

print_usage_instructions() {
  echo "Error: Specify the required parameters of the available options."
  echo "       Available options:"
  echo "          -d or -p (required): Select either dev mode or production mode."
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
    curl -X GET "https://api.cloudflare.com/client/v4/ips" > Backend/cloudflare_ips.json && \
    source Deployment/venv/bin/activate && \
    python3 -m Backend.fetch_repos && \
    pandoc <(curl "https://raw.githubusercontent.com/n-l-i/Simple_Password_Based_Mutual_Authentication_Protocol/main/README.md") \
            -f gfm -t html -o Frontend/Content_pages/spbmap/protocol.html
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd "$website_directory" && \
        source Deployment/venv/bin/activate && \
        gunicorn --workers 4 \
                --bind 0.0.0.0:5001 \
                --certfile Deployment/SSL_cert/fullchain.pem \
                --keyfile Deployment/SSL_cert/privkey.pem \
                --ssl-version TLSv1_2 "Backend.server:get_app()"
    else
        cd "$website_directory" && \
        source Deployment/venv/bin/activate && \
        flask --app Backend.server \
              run --host 0.0.0.0 \
                  --port 5001 \
                  --debugger \
                  --reload \
                  --cert=adhoc
    fi
) &
wait
