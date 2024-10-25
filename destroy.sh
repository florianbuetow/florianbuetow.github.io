#!/bin/bash
# Stops the containers and removes the image that was built
docker compose down build --rmi all
docker compose down preview --rmi all
