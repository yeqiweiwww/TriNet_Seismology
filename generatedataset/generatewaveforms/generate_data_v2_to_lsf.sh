#!/bin/bash
# -*- coding: utf-8 -*-


PYTHON_PATH=/home/user/miniconda3/envs/dl/bin/python

pwd

echo $(date "+%Y%m%d-%H:%M:%S")

echo "mkdir"
$PYTHON_PATH ./mkdir.py
sleep 5

for((i=1;i<=10;i++))
do 
    echo strart ${i}
    t=$(date "+%Y%m%d%H%M%S")
    echo ep${i} ${t}
    nohup $PYTHON_PATH ./gen_data.py ${t} > ./log_gen/gen${t}.log 2>&1 &
    sleep 3
done


sleep 60

wait

echo done

echo $(date "+%Y%m%d-%H:%M:%S")

