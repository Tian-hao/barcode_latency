#!/bin/bash
filen=`sed -n ${SGE_TASK_ID}p /u/home/t/tianhao/Erin/allfiles.txt`
file1=${filen/.fastq/.cuta.fastq}
file2=${file1/_R1_/_R2_}
workpath=/u/scratch/t/tianhao/Vincent/
fileo=${file1/.fastq/.sam}
filelog=${file1/.fastq/.log}
bowtie2 --very-sensitive --local -x ~/RNASeq/Fasta/hg19 -1 "$workpath"cuta/"$file1" -2 "$workpath"cuta/"$file2" -S "$workpath"bowtie2/hg19/$fileo 2> "$workpath"bowtie2/hg19/$filelog
bowtie2 --very-sensitive --local -x ~/ISS/ref/HIV       -1 "$workpath"cuta/"$file1" -2 "$workpath"cuta/"$file2" -S "$workpath"bowtie2/HIV/$fileo 2>  "$workpath"bowtie2/HIV/$filelog
