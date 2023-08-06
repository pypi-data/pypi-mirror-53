#! /bin/bash

pip3 uninstall melopero-autostart

systemctl disable melopero-autostart.service
systemctl daemon-reload

cd /home/melopero-autostart/uninstall/

USD="uninstall-scripts/"

for uninstallscript in $(ls "$USD")
do

if [ "${uninstallscript: -3}" == ".sh" ]
then
echo "Executing ${USD}${uninstallscript} ..."
source "${USD}${uninstallscript}"
fi

done

cd /home/

rm -r /home/melopero-autostart/
rm /etc/systemd/system/melopero-autostart.service

