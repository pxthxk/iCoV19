#!/usr/bin/env python

import os
import sys
from multiprocessing import Pool

# Fetch no. of processes from console with "-n" as identifier.
# Default: 1
samplesMultiprocessIdentifierIndex = sys.argv.index("-n") if "-n" in sys.argv else None
if samplesMultiprocessIdentifierIndex:
    if ((len(sys.argv)-1) > samplesMultiprocessIdentifierIndex) and sys.argv[samplesMultiprocessIdentifierIndex+1].isdigit():
        samplesMultiprocess = int(sys.argv[samplesMultiprocessIdentifierIndex+1])
    else:
        print("Invalid value for argument \"-n\".")
        sys.exit()
else:
    samplesMultiprocess = 1

# Fetch region from console with "-R" as identifier.
regionIdentifierIndex = sys.argv.index("-R") if "-R" in sys.argv else None
region = sys.argv[regionIdentifierIndex+1].replace(" ", "-") if regionIdentifierIndex and ((len(sys.argv)-1) > regionIdentifierIndex) else None

# Fetch sample(s) from console with "-S" as identifier.
sampleIdentifierIndex = sys.argv.index("-S") if "-S" in sys.argv else None
samples = sys.argv[sampleIdentifierIndex+1].split(",") if sampleIdentifierIndex and ((len(sys.argv)-1) > sampleIdentifierIndex) else None

directory = None
if region:
	if os.path.isdir("../data/Samples/regions/" + region + "/"):
		directory = "../data/Samples/regions/" + region + "/"

def processSample(SRXID):
	if os.path.isdir(directory + SRXID):
		SRXDir = directory + SRXID + "/"
		SRRID = [i for i in os.listdir(directory + SRXID) if ((i.startswith("ERR")) or (i.startswith("SRR"))) and (len(i.split(".")) == 1)][0]

		os.system("bcftools mpileup -f ../data/Datasets/NC_045512.2/NC_045512.2.fa " + SRXDir + "5-COVID-Aligned/*_deduplicated.bam | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > " + SRXDir + "5-COVID-Aligned/" + SRRID + ".fasta")
	else:
		print("Couldn't find sample \"" + SRXID + "\" for " + region.replace("-", " "))

if __name__ == "__main__":
	if directory:
		if samples:
			SRX = samples
		else:
			SRX = [i for i in os.listdir(directory) if (i.startswith("SRX")) or (i.startswith("ERX"))]

		p = Pool(samplesMultiprocess)
		p.map(processSample, SRX)
	else:
		print("None/Invalid region (-R) argument provided.")
