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
		SRRPath = SRXDir + SRRID

		if not os.path.isdir(SRXDir + "0-logs"):
			# Make subdirectories.
			os.system("mkdir " + SRXDir + "0-logs " + SRXDir + "1-Trimmomatic " + SRXDir + "2-fastqc " + SRXDir + "3-Human-Aligned " + SRXDir + "4-Human-Unaligned " + SRXDir + "5-COVID-Aligned " + SRXDir + "6-Qualimap " + SRXDir + "7-flagstat " + SRXDir + "8-Coverage")

			# SRA-Tools: SRA to fastq files.
			os.system("../tools/sratoolkit.2.10.5-ubuntu64/bin/fastq-dump --split-files " + SRRPath + " --outdir " + SRXDir)
			# os.system("../tools/sratoolkit.2.10.5-ubuntu64/bin/fasterq-dump " + SRRPath + " -O " + SRXDir)
			
			# Trimmomatic
			os.system("java -jar ../tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE " + SRRPath + "_1.fastq " + SRRPath + "_2.fastq " + SRXDir + "1-Trimmomatic/" + SRRID + "_1_paired.fastq " + SRXDir + "1-Trimmomatic/" + SRRID + "_1_unpaired.fastq " + SRXDir + "1-Trimmomatic/" + SRRID + "_2_paired.fastq " + SRXDir + "1-Trimmomatic/" + SRRID + "_2_unpaired.fastq ILLUMINACLIP:../tools/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100")

			# FastQC
			os.system("fastqc " + SRXDir + "1-Trimmomatic/" + SRRID + "_1_paired.fastq -o " + SRXDir + "2-fastqc/")
			os.system("fastqc " + SRXDir + "1-Trimmomatic/" + SRRID + "_2_paired.fastq -o " + SRXDir + "2-fastqc/")
			
			# Hisat2: Human genome alignment.
			os.system("hisat2 -x ../data/Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 " + SRXDir + "1-Trimmomatic/" + SRRID + "_1_paired.fastq -2 " + SRXDir + "1-Trimmomatic/" + SRRID + "_2_paired.fastq -S " + SRXDir + "3-Human-Aligned/" + SRRID + ".sam -p 16 --dta-cufflinks --summary-file " + SRXDir + "0-logs/Hisat2.log")

			# Human aligned SAM to BAM.
			os.system("samtools sort -@ 8 " + SRXDir + "3-Human-Aligned/" + SRRID + ".sam -o " + SRXDir + "3-Human-Aligned/" + SRRID + ".bam -O BAM")

			# Filter out unmapped reads.
			os.system("samtools view -u -f 4 -F 264 " + SRXDir + "3-Human-Aligned/" + SRRID + ".bam > " + SRXDir + "4-Human-Unaligned/temp1.bam")
			os.system("samtools view -u -f 8 -F 260 " + SRXDir + "3-Human-Aligned/" + SRRID + ".bam > " + SRXDir + "4-Human-Unaligned/temp2.bam")
			os.system("samtools view -u -f 12 -F 256 " + SRXDir + "3-Human-Aligned/" + SRRID + ".bam > " + SRXDir + "4-Human-Unaligned/temp3.bam")
			os.system("samtools merge -u - " + SRXDir + "4-Human-Unaligned/temp[123].bam | samtools sort -n -o " + SRXDir + "4-Human-Unaligned/" + SRRID + ".bam")
			os.system("rm " + SRXDir + "4-Human-Unaligned/temp1.bam " + SRXDir + "4-Human-Unaligned/temp2.bam " + SRXDir + "4-Human-Unaligned/temp3.bam")

			# Unmapped reads to fastq.
			os.system("bamToFastq -i " + SRXDir + "4-Human-Unaligned/" + SRRID + ".bam -fq " + SRXDir + "4-Human-Unaligned/" + SRRID + "_1.fastq -fq2 " + SRXDir + "4-Human-Unaligned/" + SRRID + "_2.fastq")

			# BWA: SARS-CoV-2 genome alignment.
			os.system("bwa mem ../data/Datasets/NC_045512.2/NC_045512.2.fa " + SRXDir + "4-Human-Unaligned/" + SRRID + "_1.fastq " + SRXDir + "4-Human-Unaligned/" + SRRID + "_2.fastq > " + SRXDir + "5-COVID-Aligned/" + SRRID + ".sam")

			# SARS-CoV-2 aligned SAM to BAM.
			os.system("samtools sort -@ 8 " + SRXDir + "5-COVID-Aligned/" + SRRID + ".sam -o " + SRXDir + "5-COVID-Aligned/" + SRRID + ".bam -O BAM")

			# Picard: Remove duplicates.
			os.system("java -jar ../tools/Picard/picard.jar MarkDuplicates I=" + SRXDir + "5-COVID-Aligned/" + SRRID + ".bam O=" + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam M=" + SRXDir + "5-COVID-Aligned/" + SRRID + "_duplicates.txt REMOVE_DUPLICATES=true USE_JDK_DEFLATER=true USE_JDK_INFLATER=true")

			# Generate SARS-CoV-2 aligned consensus FASTA
			os.system("bcftools mpileup -f ../data/Datasets/NC_045512.2/NC_045512.2.fa " + SRXDir + "5-COVID-Aligned/*_deduplicated.bam | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > " + SRXDir + "5-COVID-Aligned/" + SRRID + ".fasta")

			# Qualimap
			os.system("../tools/qualimap_v2.2.1/qualimap bamqc -bam " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam -outdir " + SRXDir + "6-Qualimap/")

			# Flagstat
			os.system("samtools flagstat " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam > " + SRXDir + "7-flagstat/" + SRRID + ".stats")

			# SARS-CoV-2 aligned sample coverage.
			os.system("genomeCoverageBed -ibam " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam > " + SRXDir + "8-Coverage/" + SRRID + ".txt")

			# REDItools
			os.system("samtools index " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam.bai")
			if not os.path.isdir("../output/REDItools2/"):
				os.system("mkdir ../output/REDItools2/")
			if not os.path.isdir("../output/REDItools2/regions"):
				os.system("mkdir ../output/REDItools2/regions")
			if not os.path.isdir("../output/REDItools2/regions/" + region):
				os.system("mkdir ../output/REDItools2/regions/" + region)
			os.system("python ../tools/reditools2.0/src/cineca/reditools.py -f " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam -S -s 0 -os 4 -r ../data/Datasets/NC_045512.2/NC_045512.2.fa -m ../output/REDItools2/homopolymers_NC_045512.2.txt -c ../output/REDItools2/homopolymers_NC_045512.2.txt -q 33 -bq 30 -mbp 15 -Mbp 15 -o ../output/REDItools2/regions/" + region + "/" + SRXID + ".txt")

			# JACUSA
			if not os.path.isdir("../output/JACUSA/"):
				os.system("mkdir ../output/JACUSA/")
			if not os.path.isdir("../output/JACUSA/regions"):
				os.system("mkdir ../output/JACUSA/regions")
			if not os.path.isdir("../output/JACUSA/regions/" + region):
				os.system("mkdir ../output/JACUSA/regions/" + region)
			os.system("java -jar ../tools/JACUSA/JACUSA_v1.3.0.jar call-1 -r ../output/JACUSA/regions/" + region + "/" + SRXID + ".vcf -a B,I,Y -s -f V -q 30 -m 33 " + SRXDir + "5-COVID-Aligned/" + SRRID + "_deduplicated.bam")
		else:
			print(SRXID + " already processed. Skipping...")
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
