#!/bin/bash
# Builds the image (if it doesnt exist) and starts the container
PORT=8000 # If you change the port in the docker-compose.yml file, you need to change it here as well.
(sleep 1 ; open http://localhost:$PORT) &
docker compose up preview