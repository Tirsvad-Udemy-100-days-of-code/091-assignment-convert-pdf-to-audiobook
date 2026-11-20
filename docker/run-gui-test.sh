#!/bin/sh
# Runs inside the container: start a virtual display, run the window test and
# take a screenshot of the display. Output goes to the folder given as $1.
set -eu
out="${1:-/results}"
mkdir -p "$out"
Xvfb :99 -screen 0 800x500x24 >"$out/xvfb.log" 2>&1 &
export DISPLAY=:99
sleep 2
python tools/window_container_test.py --log "$out/window.log" --hold 4 --pdf /app/tests/data/sample.pdf &
test_pid=$!
sleep 3
import -window root "$out/window.png"
wait "$test_pid"
