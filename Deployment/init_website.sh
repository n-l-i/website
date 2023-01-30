#!/bin/bash

website_directory="$(realpath "$0" | xargs dirname)/.."
dev_mode=""
production_mode=""
website_url=""

print_usage_instructions() {
  echo "Error: Specify the required parameters of the available options."
  echo "       Available options:"
  echo "          -d or -p (required): Select either dev mode or production mode."
  echo "          -u value (required): Set the website URL."
}

while getopts ':dpu:' flag; do
  case "${flag}" in
    d) dev_mode="true" ;;
    p) production_mode="true" ;;
    u) website_url="${OPTARG}" ;;
    *) print_usage_instructions; exit 1 ;;
  esac
done
[[ -z "$dev_mode" && -z "$production_mode" ]] && print_usage_instructions && exit 1
[[ ! -z "$dev_mode" && ! -z "$production_mode" ]] && print_usage_instructions && exit 1
[[ -z "$website_url" ]] && print_usage_instructions && exit 1
if [[ "$website_url" != *"://"* ]]; then
    website_url="https://$website_url"
fi
if [[ "$website_url" != "http://"* && "$website_url" != "https://"* ]]; then
    echo "Error: URL \"$website_url\" is not a valid HTTP URL."
    exit 1
fi
if [[ "$website_url" == "http://"* ]]; then
    echo "Warning: URL \"$website_url\" is not a HTTPS URL."
    read -p "Do you wish to proceed anyway? (y/N): " answer
    if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
        exit 1
    fi
fi

(
    cd $website_directory && \
    sed "s;\[URL\];$website_url;g" Frontend/Landing_page/index.html > Frontend/Landing_page/index_live.html
) && (
    cd $website_directory && \
    touch Log/all_requests.txt && \
    touch Log/failed_requests.txt && \
    touch Log/non_proxied_requests.txt && \
    touch Log/successful_requests.txt
) && (
    cd $website_directory/Deployment && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    cd .. && \
    python3 -m pip install -r Backend/requirements.txt && \
    python3 -c "from Backend.database_requests import init_db;init_db()"
) && (
    if [[ ! -z "$dev_mode" ]]; then
        cd $website_directory && \
        source Deployment/venv/bin/activate && \
        python3 -m pip install cryptography
    fi
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd $website_directory && \
        source Deployment/venv/bin/activate && \
        python3 -m pip install gunicorn
    fi
) && (
    cd $website_directory && \
    openssl dhparam -dsaparam -out Deployment/SSL_cert/dhparam.pem 4096
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd $website_directory && \
        sudo apt install nginx && \
        sudo rm -f /etc/nginx/sites-enabled/default && \
        sed "s;\[WEBSITE_DIR\];$website_directory;g" Deployment/nginx_config > Deployment/nginx_config_live && \
        sudo rm -f /etc/nginx/sites-available/webserver && \
        sudo cp Deployment/nginx_config_live /etc/nginx/sites-available/webserver && \
        sudo rm -f /etc/nginx/sites-enabled/webserver && \
        sudo ln -s /etc/nginx/sites-available/webserver /etc/nginx/sites-enabled/webserver && \
        sudo systemctl restart nginx
    fi
)
