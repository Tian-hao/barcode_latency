#!/usr/bin/env python
import glob

def main():
  workpath = '/u/scratch/t/tianhao/Vincent/barcode/'
  infiles = sorted(glob.glob(workpath+'barcode*.txt'))
  countdict = {}; bclist = []
  for infile in infiles:
    sample = infile.rsplit('_')[-2]
    inhandle = open(infile)
    countdict[sample] = {}
    for line in inhandle:
      line = line.rstrip()
      if ':' in line: continue
      if line == '': line = 'empty'
      if line not in countdict[sample]:
        countdict[sample][line] = 0
      if line not in bclist:
        bclist.append(line)
      countdict[sample][line] += 1
    print('finishing '+infile)
    inhandle.close()
  outfile = open('../barcode_summary.txt','w')
  outfile.write('barcode')
  for sample in countdict:
    outfile.write('\t'+sample)
  outfile.write('\n')
  for bc in bclist:
     outfile.write(bc)
     for sample in countdict:
       if bc not in countdict[sample]:
         outfile.write('\t0')
       else:
         outfile.write('\t'+str(countdict[sample][bc]))
     outfile.write('\n')
  outfile.close()
  
if __name__ == '__main__':
  main()
