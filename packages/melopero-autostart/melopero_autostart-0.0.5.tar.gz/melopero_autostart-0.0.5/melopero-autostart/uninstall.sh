#! /bin/bash

pip3 uninstall melopero-autostart

systemctl disable melopero-autostart.service
systemctl daemon-reload

rm -r /home/melopero-autostart/
rm /etc/systemd/system/melopero-autostart.service
