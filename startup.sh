#!/bin/sh

FOLDER="/home/viktor/Desktop/G-Unit"
USER="viktor"

date >> $FOLDER/git.log

sudo -u $USER git \
	--git-dir=$FOLDER/.git \
	--work-tree=$FOLDER \
	fetch origin >> $FOLDER/git.log

sudo -u $USER git \
	--git-dir=$FOLDER/.git \
	--work-tree=$FOLDER \
	merge origin/master >> $FOLDER/git.log

date >> $FOLDER/web.log

sudo python $FOLDER/src/ui.py >> $FOLDER/web.log
