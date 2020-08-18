#!/usr/bin/env python

import os
import sys
import pandas as pd

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

outputDir = "../output/REDItools2/regions/"

directory = None
if region:
	if os.path.isdir("../data/samples/regions/" + region + "/"):
		directory = "../data/samples/regions/" + region + "/"

if samples:
	SRX = samples
else:
	SRX = [i for i in os.listdir(directory) if (i.startswith("SRX")) or (i.startswith("ERX"))]

if directory:
	df = pd.DataFrame(columns=["Sample", "Mapped Paired Reads", "Coverage", "Error Rate"], dtype=object)	

	for SRXID in SRX:
		if os.path.isdir(directory + SRXID):
			SRXDir = directory + SRXID + "/"
			
			if os.path.isdir(SRXDir + "0-logs"):
				with open(SRXDir + "6-Qualimap/genome_results.txt", "r") as qualimap:
					qualimap = qualimap.readlines()
					mappedReads = qualimap[[i for i,s in enumerate(qualimap) if "number of mapped paired reads (both in pair)" in s][0]].split("=")[-1].strip()
					coverage = qualimap[[i for i,s in enumerate(qualimap) if "mean coverageData" in s][0]].split("=")[-1].strip()
					errorRate = qualimap[[i for i,s in enumerate(qualimap) if "general error rate" in s][0]].split("=")[-1].strip()

					df.loc[len(df)] = [SRXID, mappedReads, coverage, errorRate]
			else:
				print(SRXID + " not processed. Skipping...")
		else:
			print("Couldn't find sample \"" + SRXID + "\" for " + region.replace("-", " "))

	print("Writing...")
	df.to_csv(outputDir + region.replace(" ", "-") + "/" + "Stats.tsv", index=False, sep="\t")
else:
	print("None/Invalid region (-R) argument provided.")


