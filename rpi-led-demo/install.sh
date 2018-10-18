#!/bin/sh

set -x

install_dir=/opt/rpi-led-watcher
mkdir -p $install_dir

systemctl stop led-watcher.service
systemctl disable led-watcher.service

cp -f ./led-watcher.py $install_dir
cp -f ./requirements.txt $install_dir
cp -f ./systemd/start.sh $install_dir

cp -f ./systemd/led-watcher.service /etc/systemd/system/led-watcher.service

cd $install_dir
#pipenv install -r requirements.txt
pip3 install -r requirements.txt

systemctl daemon-reload
systemctl enable led-watcher.service
systemctl start led-watcher.service
