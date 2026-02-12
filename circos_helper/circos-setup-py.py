#!/usr/bin/env python

import random
import argparse
import subprocess
import re


parser = argparse.ArgumentParser(description='More efficient circos plots. You must have blast and prodigal installed.')
parser.add_argument('--reference', metavar= 'FILE', help="REQUIRED-The reference genome file")
parser.add_argument('--query', metavar = 'FILE', help="REQUIRED-The query genome file")
parser.add_argument('--qscale', nargs='?', metavar = 'string', default = "1.0", help="Optional-The scale for query, default 1.0. Enter with decimal point.")
parser.add_argument('--rscale', nargs='?', metavar = 'string', default = "1.0", help="Optional-The scale for reference, default 1.0. Enter with decimal point.")
parser.add_argument('--rColor', nargs='?', metavar = 'string', default = "0,0,0", help="Optional-The color for the reference contigs, put r,g,b, e.g. 0,0,0 (default)")
parser.add_argument('--qColor', nargs='?', metavar = 'string', default = "255,0,0", help="Optional-The color for the query contigs, put r,g,b, e.g. 255,0,0 (default)")
parser.add_argument('--Color0', nargs = '?', metavar = 'string', default = "set1-8-qual-6", help="Optional-enter color code for 0-50%%, e.g. set1-8-qual-6 (default)")
parser.add_argument('--Color50', nargs = '?', metavar = 'string', default = "set1-8-qual-3", help="Optional-enter color code for 50%%-70%%, e.g. set1-8-qual-3 (default)")
parser.add_argument('--Color70', nargs = '?', metavar = 'string', default = "rdbu-9-div-9", help="Optional-enter color code for 70%%-90%%, e.g. rdbu-9-div-9 (default)")
parser.add_argument('--Color90', nargs = '?', metavar = 'string', default = "reds-8-seq-8", help="Optional-enter color code for >90%%, e.g. reds-8-seq-8 (default)")
args = parser.parse_args()
rIndex_list = []
qIndex_list = []
r_size_dic={}
q_size_dic={}
r_size = []
q_size = []
r_index = 0
q_index = 0



# This is processing the reference file. This is simply going to change whatever the contigs are called to something real simple, so it can be processed much more easily. It writes to a new file, named reference.fasta which I will run through prodigal later in the bash script so I can get a clearly-named protein file, which I will process using bash. The very last section checks for end of file which is handy when working with single contig files.

def make_r_file(r_text,r_out_text):
	previous = ''
	gene_line = ''
	prev_line = ''
	f2 = open(r_out_text,'w')
	with open(r_text,'r') as f1:
	
		line = None
		for line in f1:

			if ">" in line:
				if prev_line != '':
					f2.write(gene_line + "\n")
					r_size.append(len(gene_line.strip()))
					r_size_dic[r_index] = len(gene_line.strip())
				r_index = random.randint(100000,999999)
				while r_index in rIndex_list:
					r_index = random.randint(100000,999999)
				rIndex_list.append(r_index)
				replacement= ">RE00_" + str(r_index) + "\n"				
				f2.write((line.replace(line,replacement)))
				gene_line = ''
			
			else:	 
				gene_line = gene_line + line.strip()
				prev_line = line

		if line is not None:
			
			f2.write(gene_line.strip())
			r_size.append(len(gene_line.strip()))
			#
			r_size_dic[r_index] = len(gene_line.strip())
				
	f1.close()
	f2.close()				
	return (r_out_text)

# This section is for processing the query file. The same as the reference file, it changes the name so it'll be simple to process nad gives the output as query.fasta. Also checks for end of file at the end, to process the last line slightly differently. This comes in quite handy.

def make_q_file(q_text,q_out_text):
	previous = ''
	gene_line = ''
	prev_line = ''
	f2 = open(q_out_text,'w')
	with open(q_text,'r') as f1:
	
		line = None
		for line in f1:

			if ">" in line:
				if prev_line != '':
					f2.write(gene_line + "\n")
					q_size.append(len(gene_line.strip()))
					q_size_dic[q_index] = len(gene_line.strip())
				q_index = random.randint(1000,9999)
				while q_index in qIndex_list:
					q_index = random.randint(1000,9999)
				qIndex_list.append(q_index)
				
				replacement= ">QU_" + str(q_index) + "\n"				
				f2.write((line.replace(line,replacement)))
				gene_line = ''
			
			else:	 
				gene_line = gene_line + line.strip()
				prev_line = line

		if line is not None:
			
			f2.write(gene_line.strip())
			q_size.append(len(gene_line.strip()))
			q_size_dic[q_index] = len(gene_line.strip())

				
	f1.close()
	f2.close()				
	return (q_out_text)

	
r_out_text = "reference.fasta"
make_r_file(args.reference,r_out_text)	
RE_kar_file = "RE_kar.txt"
f = open(RE_kar_file,'w')

for key in r_size_dic:
	kar_list = []
	kar_line = "chr -"
	if len(r_size_dic) == 1:
		kar_list.extend(("RE0","0","0",str(r_size_dic[key]),args.rColor))
	else:
		kar_list.extend(("RE" + str(key),str(key),"0",str(r_size_dic[key]),args.rColor))
	for j in range(0,len(kar_list)): kar_line = kar_line + " " + kar_list[j]
	f.write(kar_line + "\n")

f.close()

q_out_text = "query.fasta"
make_q_file(args.query,q_out_text)
QU_kar_file = "QU_kar.txt"
f = open(QU_kar_file,'w')
	
for key in q_size_dic:
	kar_list = []
	kar_line = "chr -"
	if len(q_size_dic) == 1:
		kar_list.extend(("QU0","0","0",str(q_size_dic[key]),args.qColor))
	else:
		kar_list.extend(("QU" + str(key),str(key),"0",str(q_size_dic[key]),args.qColor))
	for j in range(0,len(kar_list)): kar_line = kar_line + " " + kar_list[j]
	f.write(kar_line + "\n")

f.close()

color0="color="+args.Color0
color50="color="+args.Color50
color70="color="+args.Color70
color90="color="+args.Color90

subprocess.check_call(["bash","circos-setup-py.sh","-R","reference.fasta","-Q","query.fasta","-a",color0,"-b",color50,"-c",color70,"-d",color90,"-r","RE_kar.txt","-q","QU_kar.txt","-p",args.rscale,"-s",args.qscale])









