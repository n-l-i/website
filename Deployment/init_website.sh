#!/bin/bash

set -e

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
if [[ -z "$dev_mode" && -z "$production_mode" ]] ||
        [[ ! -z "$dev_mode" && ! -z "$production_mode" ]] ||
        [[ -z "$website_url" ]]; then
    print_usage_instructions
    exit 1
fi

(
    cd $website_directory
    sed "s;\[URL\];https://$website_url;g" Frontend/Landing_page/index.html > Frontend/Landing_page/index_live.html

    touch Log/all_requests.txt
    touch Log/failed_requests.txt
    touch Log/non_proxied_requests.txt
    touch Log/successful_requests.txt

    if [[ ! -z "$(command -v apt)" ]]; then
        [[ -z "$(command -v curl)" ]] && sudo apt install curl
        [[ -z "$(command -v python3)" ]] && sudo apt install python3
    elif [[ ! -z "$(command -v yum)" ]]; then
        [[ -z "$(command -v curl)" ]] && sudo yum install curl
        [[ -z "$(command -v python3)" ]] && sudo yum install python3
    else
        exit 1
    fi

    cd Deployment
    python3 -m venv venv
    source venv/bin/activate
    cd ..
    python3 -m pip install -r Backend/requirements.txt
    python3 -c "from Backend.database_requests import init_db;init_db()"
    python3 -m pip install grip

    if [[ ! -z "$dev_mode" ]]; then
        python3 -m pip install selenium
        python3 -m pip install cryptography
    fi
    if [[ ! -z "$production_mode" ]]; then
        python3 -m pip install gunicorn
        if [[ -z "$(command -v nginx)" ]]; then
            deactivate
            [[ ! -z "$(command -v apt)" ]] && sudo apt install nginx
            [[ ! -z "$(command -v yum)" ]] && sudo amazon-linux-extras install "$(amazon-linux-extras | grep nginx | sed 's/.*nginx/nginx/' | sed 's/ .*//')"
            [[ -z "$(command -v apt)" && -z "$(command -v yum)" ]] && exit 1
            source Deployment/venv/bin/activate
        fi
    fi

    if [[ ! -z "$production_mode" ]]; then
        cd $website_directory
        sed "s;\[WEBSITE_DIR\];$website_directory;g" Deployment/nginx_config > Deployment/nginx_config_live
        sed -i "s;\[DOMAIN_NAME\];$website_url;g" Deployment/nginx_config_live
        if [[ ! -z "$(command -v apt)" ]]; then
            sudo mkdir -p /etc/nginx/sites-available
            sudo mkdir -p /etc/nginx/sites-enabled
            sudo rm -f /etc/nginx/sites-enabled/default
            sudo rm -f /etc/nginx/sites-available/webserver
            sudo cp Deployment/nginx_config_live /etc/nginx/sites-available/webserver
            sudo rm -f /etc/nginx/sites-enabled/webserver
            sudo ln -s /etc/nginx/sites-available/webserver /etc/nginx/sites-enabled/webserver
        elif [[ ! -z "$(command -v yum)" ]]; then
            sudo mkdir -p /etc/nginx/conf.d
            sudo rm -f /etc/nginx/conf.d/webserver.conf
            sudo cp Deployment/nginx_config_live /etc/nginx/conf.d/webserver.conf
        else
            exit 1
        fi
        if [[ ! -e "Deployment/SSL_cert/fullchain.pem" && ! -h "Deployment/SSL_cert/fullchain.pem" ]]; then
            sudo systemctl stop nginx
            (
                sudo python3 -m venv /opt/certbot/
                sudo /opt/certbot/bin/pip install --upgrade pip
                sudo /opt/certbot/bin/pip install certbot certbot-nginx
                sudo rm -f /usr/bin/certbot
                sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
            ) || exit 1
            sudo certbot --nginx --rsa-key-size 4096 --no-redirect --staple-ocsp -d "$website_url"
            sudo systemctl start nginx
            sudo cp /etc/letsencrypt/live/josefine.dev/fullchain.pem Deployment/SSL_cert/fullchain.pem
            sudo chown ec2-user: Deployment/SSL_cert/fullchain.pem
            sudo cp /etc/letsencrypt/live/josefine.dev/privkey.pem Deployment/SSL_cert/privkey.pem
            sudo chown ec2-user: Deployment/SSL_cert/privkey.pem
        fi
        sudo systemctl restart nginx
    fi
)
