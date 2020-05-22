#!/bin/bash
file1=`sed -n ${SGE_TASK_ID}p /u/home/t/tianhao/Erin/allfiles.txt`
file2=${file1/_R1_/_R2_}
workpath=/u/scratch/t/tianhao/Vincent/
fileo1=${file1/.fastq/.cuta.fastq}
fileo2=${file2/.fastq/.cuta.fastq}
/u/home/t/tianhao/.local/bin/cutadapt -a AGATCGGAAGAGC -o "$workpath"cuta/$fileo1 "$workpath"split/$file1
/u/home/t/tianhao/.local/bin/cutadapt -a AGATCGGAAGAGC -o "$workpath"cuta/$fileo2 "$workpath"split/$file2
