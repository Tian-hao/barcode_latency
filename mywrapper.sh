#!/bin/bash
#call mutations
echo $SGE_TASK_ID
python /u/home/t/tianhao/Erin/script/Mapper1_barcode.py `sed -n ${SGE_TASK_ID}p /u/home/t/tianhao/Erin/filename.txt`


