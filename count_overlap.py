#!/usr/bin/env python
infile = open('../barcode_summary.txt')
header = infile.readline().rstrip().rsplit('\t')
liblist = header[1:]
bcdict = {}
for lib in liblist:
  bcdict[lib] = []
for line in infile:
  line = line.rstrip().rsplit('\t')
  for i,count in enumerate(line[1:]):
    if float(count) > 0:
      bcdict[liblist[i]].append(line[0])
infile.close()


outfile = open('../barcode_overlap_count.txt','w')
outfile.write('sample\tbarcode_count\n')
#print barcode count
for sample in bcdict:
  outfile.write(sample+'\t'+str(len(bcdict[sample]))+'\n')
#print overlap barcode count
for sample1 in bcdict: 
  for sample2 in bcdict:
    if sample1 == sample2: continue
    outfile.write(sample1+'_and_'+sample2+'\t')
    ovcount = len(set(bcdict[sample1]).intersection(set(bcdict[sample2])))
    outfile.write(str(ovcount)+'\n')
#print overlap of 3 samples
for samplee in bcdict:
  bclist = [];splist = []
  for sample in bcdict:
    if sample!=samplee:
      bclist.append(bcdict[sample])
      splist.append(sample)
  ovcount = len(set(bclist[0]).intersection(set(bclist[1]),set(bclist[2])))
  outfile.write('_and_'.join(splist)+'\t'+str(ovcount)+'\n')
#print overlap of all samples
bclist = []
for sample in bcdict:
  bclist.append(bcdict[sample])
interlist = set(bclist[0]).intersection(set(bclist[1]),set(bclist[2]),set(bclist[3]))
ovcount = len(interlist)
outfile.write('all\t'+str(ovcount)+'\n')
outfile.close()
