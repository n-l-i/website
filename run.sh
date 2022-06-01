#!/bin/bash

(cd "$(dirname "$0")" && source venv/bin/activate && cd ..; python3 -m website.Backend.server) &
wait
