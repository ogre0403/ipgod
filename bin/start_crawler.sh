#!/bin/bash

export PATH=/opt/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#source /etc/profile
#source ~/.bash_profile

from=$(date +%s)

cd ../lib/
/opt/anaconda3/bin/python3 ./crawler.py

now=$(date +%s)
total_time=$(expr $now - $from )
