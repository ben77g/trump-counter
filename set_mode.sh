#!/bin/sh
# Usage: ./set_mode.sh open|close   -- flips mode.json (public +1 on/off), commits and pushes.
set -e
cd "$(dirname "$0")"
case "$1" in
  open)  echo '{"open": true}'  > mode.json ;;
  close) echo '{"open": false}' > mode.json ;;
  *) echo "usage: $0 open|close"; exit 1 ;;
esac
git add mode.json
git commit -q -m "Counter input: $1" || true
git push -q origin main
echo "mode: $1"
