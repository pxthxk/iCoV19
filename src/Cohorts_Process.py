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
cohort = sys.argv[cohortIdentifierIndex+1] if cohortIdentifierIndex and ((len(sys.argv)-1) > cohortIdentifierIndex) else None

# Fetch sample(s) from console with "-S" as identifier.
sampleIdentifierIndex = sys.argv.index("-S") if "-S" in sys.argv else None
samples = sys.argv[sampleIdentifierIndex+1].split(",") if sampleIdentifierIndex and ((len(sys.argv)-1) > sampleIdentifierIndex) else None

# Check if sample source is SRA with "-SRA" as identifier.
# Default: False
SRAFlag = True if "-SRA" in sys.argv else False

# Check if sample is single-end with "-SE" as identifier.
# Default: False
SEFlag = True if "-SE" in sys.argv else False

# Check if sample has viral reads only with "-VO" as identifier.
# Default: False
VOFlag = True if "-VO" in sys.argv else False

directory = None
if cohort:
	if os.path.isdir("../data/samples/cohorts/" + cohort + "/"):
		directory = "../data/samples/cohorts/" + cohort + "/"

def processSample(sampleID):
	if os.path.isdir(directory + sampleID):
		sampleDir = directory + sampleID + "/"

		if SRAFlag:
			SRRID = [i for i in os.listdir(sampleDir) if ((i.startswith("ERR")) or (i.startswith("SRR"))) and (len(i.split(".")) == 1)][0]
			samplePath = sampleDir + SRRID
		else:
			samplePath = sampleDir + sampleID

		if not os.path.isdir(sampleDir + "0-logs"):
			# Make subdirectories.
			os.system("mkdir " + sampleDir + "0-logs " + sampleDir + "1-Trimmomatic " + sampleDir + "2-fastqc " + sampleDir + "3-Human-Aligned " + sampleDir + "4-Human-Unaligned " + sampleDir + "5-COVID-Aligned " + sampleDir + "6-Qualimap " + sampleDir + "7-flagstat " + sampleDir + "8-Coverage")

			# SRA-Tools: SRA to fastq files.
			if SRAFlag:
				os.system("../tools/sratoolkit.2.10.5-ubuntu64/bin/fastq-dump --split-files " + samplePath + " --outdir " + sampleDir)
				# os.system("../tools/sratoolkit.2.10.5-ubuntu64/bin/fasterq-dump " + samplePath + " -O " + sampleDir)

			# Trimmomatic
			if SEFlag:
				os.system("java -jar ../tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE " + samplePath + "_1.fastq " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_trimmed.fastq " + "ILLUMINACLIP:../tools/Trimmomatic-0.39/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100")
			else:
				os.system("java -jar ../tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE " + samplePath + "_1.fastq " + samplePath + "_2.fastq " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_paired.fastq " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_unpaired.fastq " + sampleDir + "1-Trimmomatic/" + sampleID + "_2_paired.fastq " + sampleDir + "1-Trimmomatic/" + sampleID + "_2_unpaired.fastq ILLUMINACLIP:../tools/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100")

			# FastQC
			if SEFlag:
				os.system("fastqc " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_trimmed.fastq -o " + sampleDir + "2-fastqc/")
			else:
				os.system("fastqc " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_paired.fastq -o " + sampleDir + "2-fastqc/")
				os.system("fastqc " + sampleDir + "1-Trimmomatic/" + sampleID + "_2_paired.fastq -o " + sampleDir + "2-fastqc/")
			
			if not VOFlag:
				# Hisat2: Human genome alignment.
				if SEFlag:
					os.system("hisat2 -x ../data/datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -U " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_trimmed.fastq -S " + sampleDir + "3-Human-Aligned/" + sampleID + ".sam -p 16 --dta-cufflinks --summary-file " + sampleDir + "0-logs/Hisat2.log")
				else:
					os.system("hisat2 -x ../data/datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 " + sampleDir + "1-Trimmomatic/" + sampleID + "_1_paired.fastq -2 " + sampleDir + "1-Trimmomatic/" + sampleID + "_2_paired.fastq -S " + sampleDir + "3-Human-Aligned/" + sampleID + ".sam -p 16 --dta-cufflinks --summary-file " + sampleDir + "0-logs/Hisat2.log")

				# Human aligned SAM to BAM.
				os.system("samtools sort -@ 8 " + sampleDir + "3-Human-Aligned/" + sampleID + ".sam -o " + sampleDir + "3-Human-Aligned/" + sampleID + ".bam -O BAM")

				# Filter out unmapped reads.
				if SEFlag:
					os.system("samtools view -u -f 4 " + sampleDir + "3-Human-Aligned/" + sampleID + ".bam > " + sampleDir + "4-Human-Unaligned/" + sampleID + ".bam")
				else:
					os.system("samtools view -u -f 4 -F 264 " + sampleDir + "3-Human-Aligned/" + sampleID + ".bam > " + sampleDir + "4-Human-Unaligned/temp1.bam")
					os.system("samtools view -u -f 8 -F 260 " + sampleDir + "3-Human-Aligned/" + sampleID + ".bam > " + sampleDir + "4-Human-Unaligned/temp2.bam")
					os.system("samtools view -u -f 12 -F 256 " + sampleDir + "3-Human-Aligned/" + sampleID + ".bam > " + sampleDir + "4-Human-Unaligned/temp3.bam")
					os.system("samtools merge -u - " + sampleDir + "4-Human-Unaligned/temp[123].bam | samtools sort -n -o " + sampleDir + "4-Human-Unaligned/" + sampleID + ".bam")
					os.system("rm " + sampleDir + "4-Human-Unaligned/temp1.bam " + sampleDir + "4-Human-Unaligned/temp2.bam " + sampleDir + "4-Human-Unaligned/temp3.bam")

				# Unmapped reads to fastq.
				if SEFlag:
					os.system("bamToFastq -i " + sampleDir + "4-Human-Unaligned/" + sampleID + ".bam -fq " + sampleDir + "4-Human-Unaligned/" + sampleID + "_1.fastq")
				else:
					os.system("bamToFastq -i " + sampleDir + "4-Human-Unaligned/" + sampleID + ".bam -fq " + sampleDir + "4-Human-Unaligned/" + sampleID + "_1.fastq -fq2 " + sampleDir + "4-Human-Unaligned/" + sampleID + "_2.fastq")

				# BWA: SARS-CoV-2 genome alignment.
				if SEFlag:
					os.system("bwa mem ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + "4-Human-Unaligned/" + sampleID + "_1.fastq > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".sam")
				else:
					os.system("bwa mem ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + "4-Human-Unaligned/" + sampleID + "_1.fastq " + sampleDir + "4-Human-Unaligned/" + sampleID + "_2.fastq > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".sam")
			else:
				# BWA: SARS-CoV-2 genome alignment.
				if SEFlag:
					os.system("bwa mem ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + SRRID + "_1.fastq > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".sam")
				else:
					os.system("bwa mem ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + SRRID + "_1.fastq " + sampleDir + SRRID + "_2.fastq > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".sam")

			# SARS-CoV-2 aligned SAM to BAM.
			os.system("samtools sort -@ 8 " + sampleDir + "5-COVID-Aligned/" + sampleID + ".sam -o " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam -O BAM")

			# Picard: Remove duplicates.
			if not SEFlag:
				os.system("java -jar ../tools/Picard/picard.jar MarkDuplicates I=" + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam O=" + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam M=" + sampleDir + "5-COVID-Aligned/" + sampleID + "_duplicates.txt REMOVE_DUPLICATES=true USE_JDK_DEFLATER=true USE_JDK_INFLATER=true")

			# Generate SARS-CoV-2 aligned consensus FASTA
			if SEFlag:
				os.system("bcftools mpileup -f ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".fasta")
			else:
				os.system("bcftools mpileup -f ../data/datasets/NC_045512.2/NC_045512.2.fa " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > " + sampleDir + "5-COVID-Aligned/" + sampleID + ".fasta")

			# Qualimap
			if SEFlag:
				os.system("../tools/qualimap_v2.2.1/qualimap bamqc -bam " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam -outdir " + sampleDir + "6-Qualimap/")
			else:
				os.system("../tools/qualimap_v2.2.1/qualimap bamqc -bam " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam -outdir " + sampleDir + "6-Qualimap/")

			# Flagstat
			if SEFlag:
				os.system("samtools flagstat " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam > " + sampleDir + "7-flagstat/" + sampleID + ".stats")
			else:
				os.system("samtools flagstat " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam > " + sampleDir + "7-flagstat/" + sampleID + ".stats")

			# SARS-CoV-2 aligned sample coverage.
			if SEFlag:
				os.system("genomeCoverageBed -ibam " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam > " + sampleDir + "8-Coverage/" + sampleID + ".txt")
			else:
				os.system("genomeCoverageBed -ibam " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam > " + sampleDir + "8-Coverage/" + sampleID + ".txt")

			# REDItools
			if not os.path.isdir("../output/REDItools2/"):
				os.system("mkdir ../output/REDItools2/")
			if not os.path.isdir("../output/REDItools2/cohorts"):
				os.system("mkdir ../output/REDItools2/cohorts")
			if not os.path.isdir("../output/REDItools2/cohorts/" + cohort):
				os.system("mkdir ../output/REDItools2/cohorts/" + cohort)
			if SEFlag:
				os.system("samtools index " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam.bai")
				os.system("python ../tools/reditools2.0/src/cineca/reditools.py -f " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam -S -s 0 -os 4 -r ../data/datasets/NC_045512.2/NC_045512.2.fa -m ../output/REDItools2/homopolymers_NC_045512.2.txt -c ../output/REDItools2/homopolymers_NC_045512.2.txt -q 33 -bq 30 -mbp 15 -Mbp 15 -o ../output/REDItools2/cohorts/" + cohort + "/" + sampleID + ".txt")
			else:
				os.system("samtools index " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam.bai")
				os.system("python ../tools/reditools2.0/src/cineca/reditools.py -f " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam -S -s 0 -os 4 -r ../data/datasets/NC_045512.2/NC_045512.2.fa -m ../output/REDItools2/homopolymers_NC_045512.2.txt -c ../output/REDItools2/homopolymers_NC_045512.2.txt -q 33 -bq 30 -mbp 15 -Mbp 15 -o ../output/REDItools2/cohorts/" + cohort + "/" + sampleID + ".txt")

			# JACUSA
			if not os.path.isdir("../output/JACUSA/"):
				os.system("mkdir ../output/JACUSA/")
			if not os.path.isdir("../output/JACUSA/cohorts"):
				os.system("mkdir ../output/JACUSA/cohorts")
			if not os.path.isdir("../output/JACUSA/cohorts/" + cohort):
				os.system("mkdir ../output/JACUSA/cohorts/" + cohort)
			if SEFlag:
				os.system("java -jar ../tools/JACUSA/JACUSA_v1.3.0.jar call-1 -r ../output/JACUSA/cohorts/" + cohort + "/" + sampleID + ".vcf -a B,I,Y -s -f V -q 30 -m 33 " + sampleDir + "5-COVID-Aligned/" + sampleID + ".bam")
			else:
				os.system("java -jar ../tools/JACUSA/JACUSA_v1.3.0.jar call-1 -r ../output/JACUSA/cohorts/" + cohort + "/" + sampleID + ".vcf -a B,I,Y -s -f V -q 30 -m 33 " + sampleDir + "5-COVID-Aligned/" + sampleID + "_deduplicated.bam")
		else:
			print(sampleID + " already processed. Skipping...")
	else:
		print("Couldn't find sample \"" + sampleID + "\" for " + cohort.replace("-", " "))

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
