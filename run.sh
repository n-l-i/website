#!/bin/bash
(cd "$(dirname "$0")" && python3 Backend/server.py) &
if which xdg-open > /dev/null
then
  xdg-open "http://localhost:5000/"
fi
wait
