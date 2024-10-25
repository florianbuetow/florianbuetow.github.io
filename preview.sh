#!/bin/bash
PORT=8000
(sleep 1 ; open http://localhost:$PORT) &
python3 -m http.server $PORT -d ./docs/
