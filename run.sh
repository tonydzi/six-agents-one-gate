#!/bin/sh
# One command for the stage: ./run.sh   (rehearsal: ./run.sh --down grok · backup: ./run.sh --replay recordings/best)
cd "$(dirname "$0")" && exec python3 demo.py "$@"
