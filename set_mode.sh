#!/bin/sh
# Usage: ./set_mode.sh exempt [YYYY-MM-DD]   open the public +1 for ONE lecture day (default: today if it is a lecture day,
#                                            otherwise the next one). The page closes itself again after that date.
#        ./set_mode.sh clear                 cancel an exemption.
# Writes mode.json {"open_for": "<date>"}, commits and pushes. Lecture days: Tue/Thu (ISO weekday 2 or 4) up to 2026-12-01.
set -e
cd "$(dirname "$0")"
LAST=2026-12-01
case "$1" in
  clear) D=null ;;
  exempt)
    D="$2"
    if [ -z "$D" ]; then
      i=0
      while [ $i -le 14 ]; do
        c=$(TZ=America/Toronto date -d "+$i day" +%F); w=$(TZ=America/Toronto date -d "+$i day" +%u)
        if { [ "$w" = 2 ] || [ "$w" = 4 ]; } && [ "$c" \< "$LAST" -o "$c" = "$LAST" ]; then D=$c; break; fi
        i=$((i+1))
      done
    fi
    [ -n "$D" ] || { echo "no lecture day found"; exit 1; }
    ;;
  *) echo "usage: $0 exempt [date] | clear"; exit 1 ;;
esac
if [ "$D" = null ]; then echo '{"open_for": null}' > mode.json; else echo "{\"open_for\": \"$D\"}" > mode.json; fi
git add mode.json
git commit -q -m "Counter input: exemption $D" || true
git push -q origin main
echo "public counter open for: $D"
