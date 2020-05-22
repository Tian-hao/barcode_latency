#!/usr/bin/env python
import glob

def main():
  outfile = open('../mapping_summary_bowtie2.txt','w')
  infiles = sorted(glob.glob('/u/scratch/t/tianhao/Vincent/bowtie2/hg19/*.log'))
  depdict = {}
  humdict = {}
  hivdict = {}
  for humanfile in infiles:
    sample = humanfile.rsplit('/')[-1].rsplit('_')
    sample = sample[0]+'_'+sample[1]
    if sample not in depdict:
      depdict[sample] = 0
      humdict[sample] = 0
      hivdict[sample] = 0
    hivfile = humanfile.replace('hg19','HIV')
    depth1, humanread = readlog(humanfile)
    depth2, hivread = readlog(hivfile)
    assert depth1 == depth2
    depdict[sample] += depth1
    humdict[sample] += humanread
    hivdict[sample] += hivread
  outfile.write('sample\tread_depth\thuman_genome_mapping_rate\tHIV_mapping_rate\n')
  for sample in depdict:
    outfile.write(sample+'\t'+str(depdict[sample])+'\t'+str(humdict[sample]/depdict[sample])+'\t'+str(hivdict[sample]/depdict[sample])+'\n')
  outfile.close()

def readlog(infile):
    inhandle = open(infile)
    for line in inhandle:
      if ' reads; of these:'in line: depth = line.rsplit(' ')[0]
      if 'overall alignment rate' in line: mapr = line.rsplit('%')[0]
    inhandle.close()
    return float(depth),float(depth)*float(mapr)/100
    


if __name__ == '__main__':
  main()
