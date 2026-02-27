#!/bin/bash
# -*- coding: utf-8 -*-

PYTHON_PATH=/home/user/miniconda3/envs/dl/bin/python


echo $(pwd)

echo begin

echo $(date "+%Y%m%d-%H:%M:%S")

$PYTHON_PATH ./rebuild_mkdir.py

proc_num=10
pre_model_dic_path=$(pwd)
pre_model_dic_path=$(dirname "${pre_model_dic_path}")
pre_model_dic_path="${pre_model_dic_path//generatedata_v/data/generatedata_v}/modify_tzfile"

pre_model_files=($(ls "$pre_model_dic_path"))

num=$(( (${#pre_model_files[@]} + proc_num - 1) / proc_num ))

i=0
while (( ${#pre_model_files[@]} > 0 )); do
    if (( ${#pre_model_files[@]} > num )); then
        txt=""
        for (( j=0; j<num; j++ )); do
            txt+="${pre_model_files[0]},"
            unset 'pre_model_files[0]'
            pre_model_files=("${pre_model_files[@]}")
        done
    else
        txt=""
        for file in "${pre_model_files[@]}"; do
            txt+="$file,"
        done
        pre_model_files=()
    fi

    echo ${i}

    mkdir -p ./files_list
    file_list_path="./files_list/file_list_$i.txt"
    echo "$txt" > "$file_list_path"

    mkdir -p ./log_rebuild
    nohup ./rebuild_use.py "$file_list_path" "$i" > ./log_rebuild/log_rebui$i.log 2>&1 &
    sleep  1
    
    (( i++ ))
done

wait
echo "All subprocesses are finished."
echo $(date "+%Y%m%d-%H:%M:%S")
