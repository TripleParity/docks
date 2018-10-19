#!/bin/sh

set -x

install_dir=/opt/rpi-led-watcher

systemctl stop led-watcher
systemctl disable led-watcher

rm -fr $install_dir
rm -f /etc/systemd/system/led-watcher.service
