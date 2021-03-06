#!/usr/bin/python
#Using the table generated by Meta-RNA (using the HMM3 libraries for subunit prediction) and a FASTQ file
#Version 2.0 - modified to utilize dictionaries and active memory to increase speed

from Bio import SeqIO
import sys
from collections import defaultdict

if len(sys.argv) != 7:
        print "Usage: MetaRNA_to_FastQ.py -r <output table from Meta-RNA using HMM3 libraries> -q <FASTQ file(s) searched by Meta-RNA> -o <prefix for output>"
        sys.exit()

#Variables that will be used as files

rndata = open(str(sys.argv[2]), "r")
seq_in = open(str(sys.argv[4]), "r")
out_fasta = str(sys.argv[6])+".metagenome16S.fastq"


rnaloc = defaultdict(list)

#Using the Meta-RNA output table, populates a list that contains all the IDs of the target sequences [rnaid] for quicker
#screening of the reads during the Seq IO parse.
#And creates a defaultdict [rnaloc] that uses the sequence IDs as the key and then a list as the values. The list
#contains the start and stop locations of the predicted 16S fragment
for line in rndata:
#Skip the fist line 
        if str(line[:3]) != 'seq':
                s = line.split('\t')
#ID key and append the start location
                rnaloc[s[0]].append(s[3])
#ID key and append the end location                
                rnaloc[s[0]].append(s[4])

#Parse the input FASTQ file using the data from the Meta-RNA table                
#Record list
sub_record=[]
for record in SeqIO.parse(seq_in, 'fastq'):
#Check for current seq ID in ID list
        try:
                if len(rnaloc[record.description]) > 0:
                        pos = rnaloc[record.description]
                        #Start value determined for slicing a string
                        start = int(pos[0])-1
                        #End value
                        end = int(pos[1])
                        sub_record.append(record[start:end])
#                        print str(record.id)
        except KeyError:
                continue
        except IndexError:
                print str(record.description), str(rnaloc[record.description])
                
SeqIO.write(sub_record, out_fasta, 'fastq')