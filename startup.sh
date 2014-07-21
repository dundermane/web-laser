#!/bin/sh

date >> /home/pi/weblog/git.txt

sudo -u pi -i git \
	--git-dir=./web-laser/.git \
	--work-tree=./web-laser \
	fetch origin \
	>> /home/pi/weblog/git.txt

sudo -u pi -i git \
	--git-dir=/home/pi/web-laser/.git \
	--work-tree=/home/pi/web-laser \
	merge origin/master \
	>> /home/pi/weblog/git.txt

date >> /home/pi/weblog/logs.txt
sudo python /home/pi/web-laser/src/ui.py >> /home/pi/weblog/logs.txt &
