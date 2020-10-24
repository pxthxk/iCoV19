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

directory = None
if region:
	if os.path.isdir("../data/samples/regions/" + region + "/"):
		directory = "../data/samples/regions/" + region + "/"

if samples:
	SRX = samples
else:
	SRX = [i for i in os.listdir(directory) if (i.startswith("SRX")) or (i.startswith("ERX"))]

if directory:
	df = pd.DataFrame(columns=["Sample", "Total Reads After Trimming", "Hisat2 Human Mapped Reads", "Hisat2 Human Unmapped Reads", "Hisat2 % Human Mapped Reads", "Total Reads After Removing Duplicates", "BWA-MEM SARS-CoV-2 Mapped Reads", "BWA % SARS-CoV-2 Mapped Reads", "Mean of Coverage Depth", "Standard Deviation of Coverage Depth", "Mean Mapping Quality", "GC Percentage", "Error Rate"], dtype=object)

	for SRXID in SRX:
		SRXDir = directory + SRXID + "/"
			
		try:
			with open(SRXDir + "0-logs/Hisat2.log", "r") as hisat2:
				hisat2 = hisat2.readlines()
				trimmedReads = int(hisat2[[i for i,s in enumerate(hisat2) if "reads; of these:" in s][0]].split(" reads; of these:")[0])*2
				hisat2PercentMappedReads = hisat2[[i for i,s in enumerate(hisat2) if "overall alignment rate" in s][0]].split(" overall alignment rate")[0]
				hisat2MappedReads = int((trimmedReads*float(hisat2PercentMappedReads.split("%")[0]))/100)
				hisat2UnmappedReads = int(trimmedReads) - int(hisat2MappedReads)
		except:
			trimmedReads = "-"
			hisat2MappedReads = "-"
			hisat2UnmappedReads = "-"
			hisat2PercentMappedReads = "-"
		try:
			with open(SRXDir + "6-Qualimap/genome_results.txt", "r") as qualimap:
				qualimap = qualimap.readlines()
				deduplicatedReads = "".join(qualimap[[i for i,s in enumerate(qualimap) if "number of reads" in s][0]].split("=")[-1].strip().split(","))
				bwaMappedReads = "".join(qualimap[[i for i,s in enumerate(qualimap) if "number of mapped reads" in s][0]].split("=")[-1].strip().split(" ")[0].split(","))
				bwaPercentMappedReads = qualimap[[i for i,s in enumerate(qualimap) if "number of mapped reads" in s][0]].split("=")[-1].strip().split(" ")[1].split("(")[1].split(")")[0]
				bwaMeanCoverage = qualimap[[i for i,s in enumerate(qualimap) if "mean coverageData" in s][0]].split("=")[-1].strip()
				bwaStdCoverage = qualimap[[i for i,s in enumerate(qualimap) if "std coverageData" in s][0]].split("=")[-1].strip()
				bwaMeanMappingQuality = qualimap[[i for i,s in enumerate(qualimap) if "mean mapping quality" in s][0]].split("=")[-1].strip()
				bwaGCPercent = qualimap[[i for i,s in enumerate(qualimap) if "GC percentage" in s][0]].split("=")[-1].strip()
				bwaErrorRate = qualimap[[i for i,s in enumerate(qualimap) if "general error rate" in s][0]].split("=")[-1].strip()
		except:
			deduplicatedReads = "-"
			bwaMappedReads = "-"
			bwaPercentMappedReads = "-"
			bwaMeanCoverage = "-"
			bwaStdCoverage = "-"
			bwaMeanMappingQuality = "-"
			bwaGCPercent = "-"
			bwaErrorRate = "-"

		df.loc[len(df)] = [SRXID, trimmedReads, hisat2MappedReads, hisat2UnmappedReads, hisat2PercentMappedReads, deduplicatedReads, bwaMappedReads, bwaPercentMappedReads, bwaMeanCoverage, bwaStdCoverage, bwaMeanMappingQuality, bwaGCPercent, bwaErrorRate]

	print("Writing...")
	df.to_csv(directory + "Stats.tsv", index=False, sep="\t")
else:
	print("None/Invalid region (-R) argument provided.")
	