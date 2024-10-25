#!/bin/bash
# Builds the image (if it doesnt exist) and starts the container
PORT=8000 # If you change the port in the docker-compose.yml file, you need to change it here as well.
(sleep 1 ; open http://localhost:$PORT) &
docker compose up preview

# Alternative to docker compose up preview you can use the following command to start a local server with python
# python3 -m http.server $PORT -d ./docs/
