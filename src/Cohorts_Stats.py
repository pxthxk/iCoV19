#!/usr/bin/env python

import os
import sys
import json
import re
import datetime
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

# Fetch BioProject from console with "-B" as identifier.
bioprojectIdentifierIndex = sys.argv.index("-B") if "-B" in sys.argv else None
bioproject = sys.argv[bioprojectIdentifierIndex+1] if bioprojectIdentifierIndex and ((len(sys.argv)-1) > bioprojectIdentifierIndex) else None

# Fetch cohort from console with "-C" as identifier.
if bioproject:
	cohort = bioproject
else:
	cohortIdentifierIndex = sys.argv.index("-C") if "-C" in sys.argv else None
	cohort = sys.argv[cohortIdentifierIndex+1].replace(" ", "-") if cohortIdentifierIndex and ((len(sys.argv)-1) > cohortIdentifierIndex) else None

# Fetch sample(s) from console with "-S" as identifier.
sampleIdentifierIndex = sys.argv.index("-S") if "-S" in sys.argv else None
samples = sys.argv[sampleIdentifierIndex+1].split(",") if sampleIdentifierIndex and ((len(sys.argv)-1) > sampleIdentifierIndex) else None

# Check if sample source is SRA with "-SRA" as identifier.
# Default: False
SRAFlag = True if "-SRA" in sys.argv else False

directory = None
if cohort:
	if os.path.isdir("../data/samples/cohorts/" + cohort + "/"):
		directory = "../data/samples/cohorts/" + cohort + "/"

if samples:
	samples = samples
else:
	samples = [i for i in os.listdir(directory) if os.path.isdir(os.path.join(directory, i)) and not i.startswith('.')]

if SRAFlag:
	platform = "Illumina"
	countryTags = ["geo_loc_name", "geographic location (country and/or sea)", "country", "Country"]
	SRAMetadataDir = "../data/datasets/metadata/SRA/"
	SRASampleMetadata = {}

	if bioproject:
		SRAMetadataFiles = [f for f in os.listdir(SRAMetadataDir) if os.path.isfile(SRAMetadataDir + f) and f.endswith(bioproject + ".json")]
	else:
		SRAMetadataFiles = [f for f in os.listdir(SRAMetadataDir) if os.path.isfile(SRAMetadataDir + f) and f.endswith(("Illumina_paired" if platform == "Illumina" else "Nanopore") + ".json")]

	if len(SRAMetadataFiles) != 0:
		if bioproject:
			SRAMetadataFile = max(list(map(lambda x: datetime.datetime.strptime(x.split("_")[0], "%Y%m%d"), SRAMetadataFiles))).strftime("%Y%m%d") + "_" + bioproject + ".json"
		else:
			SRAMetadataFile = max(list(map(lambda x: datetime.datetime.strptime(x.split("_")[0], "%Y%m%d"), SRAMetadataFiles))).strftime("%Y%m%d") + "_" + ("Illumina_paired" if platform == "Illumina" else "Nanopore") + ".json"
		print("Using " + SRAMetadataFile)
		
		SRAMetadata = json.load(open(SRAMetadataDir + SRAMetadataFile, "r"))
		
		for i in range(0,len(SRAMetadata["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"])):
			exp = SRAMetadata["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"][i]

			sample_platform = ""
			collection_date = ""
			host_sex = ""
			host_age = ""

			if bioproject:
				sample_platform = exp["EXPERIMENT"]["PLATFORM"]["ILLUMINA"]["INSTRUMENT_MODEL"]

				for tag in exp["SAMPLE"]["SAMPLE_ATTRIBUTES"]["SAMPLE_ATTRIBUTE"]:
					if tag["TAG"] == "collection_date":
						collection_date = tag["VALUE"]
					if tag["TAG"] == "host_sex":
						host_sex = tag["VALUE"]
					if tag["TAG"] == "host_age":
						host_age = tag["VALUE"]
				SRASampleMetadata[exp["EXPERIMENT"]["@accession"]] = (sample_platform, collection_date, host_sex, host_age)
			else:
				flag = 0
				
				for tag in exp["SAMPLE"]["SAMPLE_ATTRIBUTES"]["SAMPLE_ATTRIBUTE"]:
					if tag["TAG"] in countryTags:
						if re.search(cohort.replace("-", " ") , tag["VALUE"], re.IGNORECASE):
							flag = 1
							break
				if flag == 1:
					sample_platform = exp["EXPERIMENT"]["PLATFORM"]["ILLUMINA"]["INSTRUMENT_MODEL"]

					for tag in exp["SAMPLE"]["SAMPLE_ATTRIBUTES"]["SAMPLE_ATTRIBUTE"]:
						if tag["TAG"] == "collection_date":
							collection_date = tag["VALUE"]
						if tag["TAG"] == "host_sex":
							host_sex = tag["VALUE"]
						if tag["TAG"] == "host_age":
							host_age = tag["VALUE"]
				
					SRASampleMetadata[exp["EXPERIMENT"]["@accession"]] = (sample_platform, collection_date, host_sex, host_age)
else:
	try:
		sampleMetadata = json.load(open("../data/datasets/metadata/" + cohort + ".json", "r"))
	except:
		sampleMetadata = {}

if directory:
	df = pd.DataFrame(columns=["Sample", "Total Reads After Trimming", "Hisat2 Human Mapped Reads", "Hisat2 Human Unmapped Reads", "Hisat2 % Human Mapped Reads", "Total Reads After Removing Duplicates", "BWA-MEM SARS-CoV-2 Mapped Reads", "BWA % SARS-CoV-2 Mapped Reads", "Mean of Coverage Depth", "Standard Deviation of Coverage Depth", "Mean Mapping Quality", "GC Percentage", "Error Rate", "Platform", "Collection Date", "Gender", "Age", "Ct Value (N gene)", "Ct Value (ORF1 gene)", "Ct Value (S gene)"], dtype=object)

	for sampleID in samples:
		sampleDir = directory + sampleID + "/"
			
		try:
			with open(sampleDir + "0-logs/Hisat2.log", "r") as hisat2:
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
			with open(sampleDir + "6-Qualimap/genome_results.txt", "r") as qualimap:
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

		if SRAFlag:
			sample_platform = SRASampleMetadata[sampleID][0] if SRASampleMetadata[sampleID][0] != "" else "-"
			collection_date = SRASampleMetadata[sampleID][1] if SRASampleMetadata[sampleID][1] != "" else "-"
			host_sex = SRASampleMetadata[sampleID][2] if SRASampleMetadata[sampleID][2] != "" else "-"
			host_age = SRASampleMetadata[sampleID][3] if SRASampleMetadata[sampleID][3] != "" else "-"
			Ct_N_gene = "-"
			Ct_ORF1_gene = "-"
			Ct_S_gene = "-"
			
		else:
			if sampleID in sampleMetadata:
				sample_platform = sampleMetadata[sampleID]["platform"] if "platform" in sampleMetadata[sampleID] else "-"
				collection_date = sampleMetadata[sampleID]["collection_date"] if "collection_date" in sampleMetadata[sampleID] else "-"
				host_sex = sampleMetadata[sampleID]["sex"] if "sex" in sampleMetadata[sampleID] else "-"
				host_age = sampleMetadata[sampleID]["age"] if "age" in sampleMetadata[sampleID] else "-"
				Ct_N_gene = sampleMetadata[sampleID]["Ct_N_gene"] if "Ct_N_gene" in sampleMetadata[sampleID] else "-"
				Ct_ORF1_gene = sampleMetadata[sampleID]["Ct_ORF1_gene"] if "Ct_ORF1_gene" in sampleMetadata[sampleID] else "-"
				Ct_S_gene = sampleMetadata[sampleID]["Ct_S_gene"] if "Ct_S_gene" in sampleMetadata[sampleID] else "-"
			else:
				sample_platform = "-"
				collection_date = "-"
				host_sex = "-"
				host_age = "-"
				Ct_N_gene = "-"
				Ct_ORF1_gene = "-"
				Ct_S_gene = "-"

		df.loc[len(df)] = [sampleID, trimmedReads, hisat2MappedReads, hisat2UnmappedReads, hisat2PercentMappedReads, deduplicatedReads, bwaMappedReads, bwaPercentMappedReads, bwaMeanCoverage, bwaStdCoverage, bwaMeanMappingQuality, bwaGCPercent, bwaErrorRate, sample_platform, collection_date, host_sex, host_age, Ct_N_gene, Ct_ORF1_gene, Ct_S_gene]

	print("Writing...")
	df.to_csv(directory + "Stats.tsv", index=False, sep="\t")
else:
	print("None/Invalid cohort (-C) argument provided.")
	