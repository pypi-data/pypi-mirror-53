#! /bin/bash

DIR="/home/melopero-autostart/scripts/"

#check if script directory exists
if [ -d "$DIR" ]
then
#change dir to execute scripts inside their directory
cd "$DIR"

echo "[MP_AS]: starting to execute scripts..."

for script in $(ls)
do
if [ "${script: -3}" == ".py" ]
then
echo "[MP_AS]: executing  ${script}"
LOG="${script: 0: -3}.log"
if [ ! -f "$LOG" ]
then
touch "$LOG"
chmod 664 "$LOG"
fi

nohup python3 -u  "${DIR}${script}" > "$LOG" &

fi
done

#return to starting directory
cd /

else 
echo "[MP_AS]: Error: ${DIR} does not exist !"
exit 1
fi
