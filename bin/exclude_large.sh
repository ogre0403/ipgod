#!/bin/bash

export PATH=/opt/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#source /etc/profile
#source ~/.bash_profile

from=$(date +%s)

cd /data/ipgod/ipgod_git/lib/
/opt/anaconda3/bin/python3 ExcludeLargeDataset.py

now=$(date +%s)
total_time=$(expr $now - $from )
