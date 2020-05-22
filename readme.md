# mannual for Erin barcode cleanup
## 1. remove sequencing adapter AGATCGGAAGAGC
*note: Each file take ~1min*  
`module load python/2.7`  
`cutadapt_wrapper.sh`  
## 2. mapping to human and HIV genome
`module load bowtie2`  
`bowtie_wrapper.sh`  
## 3. summarize mapping rate from log files
`python sum_bowtie.py`  
HIV mapping rate is so low, try other mapping strategy. 
## 4. manually map barcode in RNA samples
`mywrapper.sh`  
*There is 60% low quality reads, which means score < 30 in barcode*  
`python Mapper2_barcode.py`
## 5. count overlap
`python count_overlap.py`
