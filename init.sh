#!/bin/bash

(cd "$(dirname "$0")" && python3 -m venv venv && source venv/bin/activate && pip3 install flask && pip3 install chess
