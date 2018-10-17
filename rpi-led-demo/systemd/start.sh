#!/bin/sh

install_dir=/opt/rpi-led-watcher

cd $install_dir

# -u is required for writing to stdout unbuffered
pipenv run python3 -u ./led-watcher.py
