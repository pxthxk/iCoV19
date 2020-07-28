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

# Fetch cohort from console with "-C" as identifier.
cohortIdentifierIndex = sys.argv.index("-C") if "-C" in sys.argv else None
cohort = sys.argv[cohortIdentifierIndex+1].replace(" ", "-") if cohortIdentifierIndex and ((len(sys.argv)-1) > cohortIdentifierIndex) else None

# Fetch sample(s) from console with "-S" as identifier.
sampleIdentifierIndex = sys.argv.index("-S") if "-S" in sys.argv else None
samples = sys.argv[sampleIdentifierIndex+1].split(",") if sampleIdentifierIndex and ((len(sys.argv)-1) > sampleIdentifierIndex) else None

directory = None
if cohort:
	if os.path.isdir("../data/Samples/Cohorts/" + cohort + "/"):
		directory = "../data/Samples/Cohorts/" + cohort + "/"

def processSample(sampleID):
	if os.path.isdir(directory + sampleID):
		sampleDir = directory + sampleID + "/"

		os.system("bcftools mpileup -f ../data/Datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + "5-COVID-Aligned/*_deduplicated.bam | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".fasta")
	else:
		print("Couldn't find sample \"" + sampleDir + "\" for " + cohort.replace("-", " "))

if __name__ == "__main__":
	if directory:
		if samples:
			sampleIDs = samples
		else:
			sampleIDs = [i for i in os.listdir(directory) if not i.startswith('.')]
	
		p = Pool(samplesMultiprocess)
		p.map(processSample, sampleIDs)
	else:
		print("None/Invalid cohort (-C) argument provided.")
