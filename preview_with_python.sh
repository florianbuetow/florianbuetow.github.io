#!/bin/bash
# Starts a python simple http server to serve the files in the docs folder
PORT=8000 # If you change the port in the docker-compose.yml file, you need to change it here as well.
(sleep 1 ; open http://localhost:$PORT) &
python3 -m http.server $PORT -d ./docs/
