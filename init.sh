#!/bin/bash

(
    cd "$(dirname "$0")" && \
    sed -i "s;\[URL\];$1;g" Frontend/Landing_page/index.html && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip3 install -r Backend/requirements.txt
)

