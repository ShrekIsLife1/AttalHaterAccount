#!/bin/sh
set -e

# Support both node dist/index.js and node dist/src/index.js
if [ "$1" = "node" ] && [ "$2" = "dist/index.js" ]; then
  if [ ! -f "dist/index.js" ] && [ -f "dist/src/index.js" ]; then
    set -- node dist/src/index.js
  fi
fi

exec "$@"
