#!/bin/bash

website_directory="$(realpath "$0" | xargs dirname)"
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
    sed -i "s;\[URL\];$website_url;g" Frontend/Landing_page/index.html
) && (
    cd $website_directory && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip3 install -r Backend/requirements.txt
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd $website_directory && \
        source venv/bin/activate && \
        pip3 install gunicorn
    fi
) && (
    cd $website_directory && \
    openssl dhparam -dsaparam -out SSL_cert/dhparam.pem 4096
) && (
    if [[ ! -z "$production_mode" ]]; then
        cd $website_directory && \
        sudo apt install nginx && \
        sudo rm -f /etc/nginx/sites-enabled/default && \
        sed -i "s;\[WEBSITE_DIR\];$website_directory;g" Backend/nginx_config && \
        sudo rm -f /etc/nginx/sites-available/webserver && \
        sudo cp Backend/nginx_config /etc/nginx/sites-available/webserver && \
        sudo rm -f /etc/nginx/sites-enabled/webserver && \
        sudo ln -s /etc/nginx/sites-available/webserver /etc/nginx/sites-enabled/webserver && \
        sudo systemctl restart nginx
    fi
)
