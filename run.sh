#!/bin/bash
(
    cd "$(dirname "$0")" && \
    source venv/bin/activate && \
    python3 -m Backend.fetch_repos
) && (
    cd "$(dirname "$0")" && \
    source venv/bin/activate && \
    gunicorn --workers 4 \
             --bind 0.0.0.0:5001 \
             --certfile SSL_cert/fullchain.pem \
             --keyfile SSL_cert/privkey.pem \
             --ssl-version TLSv1_2 "Backend.server:get_app()"
) &
wait
