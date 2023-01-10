#!/bin/bash

(
    cd "$(dirname "$0")" && \
    sed -i "s;\[URL\];$1;g" Frontend/Landing_page/index.html
) && (
    cd "$(dirname "$0")" && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip3 install -r Backend/requirements.txt && \
    pip3 install gunicorn
) && (
    cd "$(dirname "$0")" && \
    openssl dhparam -dsaparam -out SSL_cert/dhparam.pem 4096
) && (
    cd "$(dirname "$0")" && \
    sudo apt install nginx && \
    sudo rm -f /etc/nginx/sites-enabled/default && \
    sed -i "s;\[WEBSITE_DIR\];$(realpath "$0" | xargs dirname);g" Backend/nginx_config && \
    sudo rm -f /etc/nginx/sites-available/webserver && \
    sudo cp Backend/nginx_config /etc/nginx/sites-available/webserver && \
    sudo rm -f /etc/nginx/sites-enabled/webserver && \
    sudo ln -s /etc/nginx/sites-available/webserver /etc/nginx/sites-enabled/webserver && \
    sudo systemctl restart nginx
)
