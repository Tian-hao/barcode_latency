#!/usr/bin/env python
import sys
from Bio.Seq import Seq
from Bio import SeqIO
from time import time
from distance import hamming
#1 hours per 625000 records (2.5M lines)

def main(): 
  workpath = '/u/scratch/t/tianhao/Vincent/'
  priseqs = {'F':'TTAGTCAGTGTATCGATA','R':'GAGATTTTCCGTTTAAAC'} 
  infile1 = workpath+'split/'+sys.argv[1]
  infile2 = infile1.replace('_R1_','_R2_')
  sample = infile1.rsplit('/')[-1].rsplit('_')
  sample = sample[0]+'_'+sample[-1].rsplit('.fastq')[0]
  outfile = open(workpath+'barcode/barcode_'+sample+'.txt','w')
  inhandle1 = open(infile1); inhandle2 = open(infile2)
  handle1 = SeqIO.parse(inhandle1,'fastq'); handle2 = SeqIO.parse(inhandle2,'fastq')
  errcount = [0,0,0,0,0]; readcount = 0
  #0: good read
  #1. unmapped
  #2. only 1 primer mapped
  #3. 2 reads mapped to the same strand 
  #4. low quality
  start_time = time()
  for record1 in handle1:
    record2 = handle2.next()
    readcount += 1
    if readcount % 100000 == 0:
      print(errcount,readcount,'Time: '+str(time()-start_time))
    #map barcode
    seq1 = str(record1.seq)
    seq2 = str(record2.seq)
    offset1_beg,offset1_end,direction1 = mapbc(seq1,priseqs)
    offset2_beg,offset2_end,direction2 = mapbc(seq2,priseqs)
    if direction1 == 'NA' or direction2 == 'NA': 
      errcount[1] += 1
      continue
    if offset1_beg == 0  or offset2_beg == 0 : 
      errcount[2] += 1
      continue
    if direction1 == direction2:
      errcount[3] += 1
      continue
    if direction1 == 'F':
      bcseq1 = seq1[offset1_beg:]
      bcseq2 = str(Seq(seq2[offset2_beg:offset2_end+offset2_beg]).reverse_complement())
      bcqual1 = record1[offset1_beg:].letter_annotations["phred_quality"]
      bcqual2 = record2[offset2_beg:offset2_end+offset2_beg].letter_annotations["phred_quality"][::-1]
    if direction2 == 'F':
      bcseq1 = seq2[offset2_beg:]
      bcseq2 = str(Seq(seq1[offset1_beg:offset1_end+offset1_beg]).reverse_complement())
      bcqual1 = record2[offset2_beg:].letter_annotations["phred_quality"]
      bcqual2 = record1[offset1_beg:offset1_end+offset1_beg].letter_annotations["phred_quality"][::-1]
    if 'N' in bcseq1 or 'N' in bcseq2: 
      errcount[4] += 1
      continue
    #bcseq1 is only 4 nucleotide 
    #bcseq2 is full length barcode
    #write barcode
    low_qs_flag = 0; unpair_flag = 0
    bcseq = ''
    for n in range(len(bcseq2)):
      if n < len(bcseq1):
        if bcseq1[n] == bcseq2[n]: bcseq += bcseq1[n]
        elif bcseq1[n] != bcseq2[n] and bcqual1[n] >= 30 and bcqual2[n] < 30: bcseq += bcseq1[n]
        elif bcseq1[n] != bcseq2[n] and bcqual1[n] < 30 and bcqual2[n] >= 30: bcseq += bcseq2[n]
        elif bcseq1[n] != bcseq2[n] and bcqual1[n] >= 30 and bcqual2[n] >= 30: unpair_flag = 1; break
        elif bcseq1[n] != bcseq2[n] and bcqual1[n] < 30 and bcqual2[n] < 30: low_qs_flag = 1; break
      else:
        if bcqual2[n] < 30: 
          low_qs_flag = 1; break
        else:
          bcseq += bcseq2[n]
    if low_qs_flag == 1: 
      errcount[4] += 1
      continue
    if unpair_flag == 1:
      errcount[3] += 1
      continue
    outfile.write(bcseq+'\n')
    errcount[0] += 1
  inhandle1.close()
  inhandle2.close()
  outfile.write('Good reads: '+str(errcount[0])+'\n')
  outfile.write('Unmapped reads: '+str(errcount[1])+'\n')
  outfile.write('1-Primer reads: '+str(errcount[2])+'\n')
  outfile.write('Unpaired reads: '+str(errcount[3])+'\n')
  outfile.write('Low quanlity reads: '+str(errcount[4])+'\n')
  outfile.close()
    
def mapbc(seq,priseqs):
  for direction in priseqs:
    priseq = priseqs[direction]
    offset1 = mapseq(seq,priseq)
    if offset1 > 0: offset1 += len(priseq)
    if direction == 'F': priseq = str(Seq(priseqs['R']).reverse_complement())
    if direction == 'R': priseq = str(Seq(priseqs['F']).reverse_complement())
    offset2 = mapseq(seq[offset1:],priseq)
    if offset1 > 0 or offset2 > 0: return offset1,offset2,direction
  return 0,0,'NA'
    

def mapseq(seq,pri):
  for offset in range(len(seq)-len(pri)):
    qseq = seq[offset:offset+len(pri)]
    if len(qseq) < len(pri): break
    if hamming(qseq,pri) <= 3:
      return offset
  return 0
      
def mapindex(tagdict,bc0):
  for bc in tagdict:
    if hamming(bc,bc0) < 3: return tagdict[bc]
  return 'NA'


if __name__ == '__main__':
  main()
