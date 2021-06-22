# iCoV19

[![DOI:10.1101/2020.12.09.417519](http://img.shields.io/badge/DOI-10.1101/2020.12.09.417519-B31B1B.svg)](https://doi.org/10.1101/2020.12.09.417519)

Spatio-temporal catalouging of intra-host variability in SARS-CoV-2 transcriptomes to provide insights on the consequence of intra-host Single Nucleotide Variations (iSNVs) on the evolution of the virus.  
  
<p align="center">
  <img src="https://github.com/pxthxk/iCoV19/blob/master/visualization/assets/RadialPlot-Countries.png?raw=true" width="512" alt="Spectrum of iSNVs in samples across populations">
</p>

## Pipeline
**Trim adaptor sequences and filter low-quality reads from downstream analysis**
```bash
$ Trimmomatic-0.39/trimmomatic-0.39.jar PE <Sample_1.fastq> <Sample_2.fastq> <Sample_1_paired.fastq> <Sample_1_unpaired.fastq> <Sample_2_paired.fastq> Sample_2_unpaired.fastq> ILLUMINACLIP:Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
```
**Get reads quality metrics using FastQC**
```bash
$ fastqc <Sample_1_paired.fastq> -o <Output Dir>
$ fastqc <Sample_2_paired.fastq> -o <Output Dir>
```
**Align reads to the human genome (GRCh37)**
```bash
$ hisat2 -x <GRCh37.primary_assembly.genome> -1 <Sample_1_paired.fastq> -2 <Sample_2_paired.fastq> -S <Sample_Human_Aligned.sam> -p 16 --dta-cufflinks --summary-file <Log File>
```
**Convert human genome aligned SAM to BAM**
```bash
$ samtools sort -@ 8 <Sample_Human_Aligned.sam> -o <Sample_Human_Aligned.bam> -O BAM
```
**Filter out the unmapped reads**
```bash
$ samtools view -u -f 4 -F 264 <Sample_Human_Aligned.bam> > <temp1.bam>
$ samtools view -u -f 8 -F 260 <Sample_Human_Aligned.bam> > <temp2.bam>
$ samtools view -u -f 12 -F 256 <Sample_Human_Aligned.bam> > <temp3.bam>
$ samtools merge -u - <temp[123].bam> | samtools sort -n -o <Sample_Human_Unaligned.bam>
```
**Convert unmapped reads to FASTQ**
```bash
$ bamToFastq -i <Sample_Human_Unaligned.bam> -fq <Sample_Human_Unaligned_1.fastq> -fq2 <Sample_Human_Unaligned_2.fastq>
```
**Align unmapped reads to the SARS-CoV-2 genome (NC_045512.2)**
```bash
$ bwa mem <NC_045512.2.fa> <Sample_Human_Unaligned_1.fastq> <Sample_Human_Unaligned_2.fastq> > <Sample_SARSCoV2_Aligned.sam>
```
**Convert SARS-CoV-2 genome aligned SAM to BAM**
```bash
$ samtools sort -@ 8 <Sample_SARSCoV2_Aligned.sam> -o <Sample_SARSCoV2_Aligned.bam> -O BAM
```
**Remove duplicate reads**
```bash
$ picard.jar MarkDuplicates I=<Sample_SARSCoV2_Aligned.bam> O=<Sample_SARSCoV2_Aligned_deduplicated.bam> M=<Sample_SARSCoV2_Aligned_duplicates.txt> REMOVE_DUPLICATES=true USE_JDK_DEFLATER=true USE_JDK_INFLATER=true
```
**Generate SARS-CoV-2 genome aligned consensus FASTA**
```bash
$ bcftools mpileup -f <NC_045512.2.fa> <Sample_SARSCoV2_Aligned_deduplicated.bam> | bcftools call -c | vcfutils.pl vcf2fq | seqtk seq -aQ64 -q20 -n N > <Sample.fasta>
```
**Get reads quality metrics using QualiMap**
```bash
$ qualimap_v2.2.1/qualimap bamqc -bam <Sample_SARSCoV2_Aligned_deduplicated.bam> -outdir <Output Dir>
```
**Get reads quality metrics using Flagstat**
```bash
$ samtools flagstat <Sample_SARSCoV2_Aligned_deduplicated.bam> > <Sample_SARSCoV2_Aligned.stats>
```
**Get SARS-CoV-2 genome aligned sample coverage**
```bash
$ genomeCoverageBed -ibam <Sample_SARSCoV2_Aligned_deduplicated.bam> > <Sample_SARSCoV2_Aligned.coverage>
```
**Call iSNVs in SARS-CoV-2 genome aligned reads**
```bash
$ samtools index <Sample_SARSCoV2_Aligned_deduplicated.bam> <Sample_SARSCoV2_Aligned_deduplicated.bam.bai>
$ python2.7 reditools2.0/src/cineca/reditools.py -f <Sample_SARSCoV2_Aligned_deduplicated.bam> -S -s 0 -os 4 -r <NC_045512.2.fa> -m <homopolymers_NC_045512.2.txt> -c <homopolymers_NC_045512.2.txt> -q 33 -bq 30 -mbp 15 -Mbp 15 -o <Sample_REDItools.txt>
```
**Filter samples and bases to get high-quality iSNVs**
```
Sample qualifying criterion:
 - Error rate < 0.005

iSNV qualifying criteria:
 - Number of minor allele reads ≥ 5
 - Base coverage ≥ 20
 - Minor allele frequency ≥ 0.005
```
