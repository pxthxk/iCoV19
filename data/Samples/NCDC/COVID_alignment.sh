java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2105.1.fastq NCDC2105.2.fastq 1-Trimmomatic/NCDC2105.1_paired.fastq 1-Trimmomatic/NCDC2105.1_unpaired.fastq 1-Trimmomatic/NCDC2105.2_paired.fastq 1-Trimmomatic/NCDC2105.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2105.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2105.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2105.1_paired.fastq -2 1-Trimmomatic/NCDC2105.2_paired.fastq -S 3-Human-Aligned/NCDC2105.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2105_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2105.sam -o 3-Human-Aligned/NCDC2105.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2105.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2105.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2105.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2105.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2105.bam -fq 4-Human-Unaligned/NCDC2105_1.fq -fq2 4-Human-Unaligned/NCDC2105_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2105_1.fq 4-Human-Unaligned/NCDC2105_2.fq > 5-COVID-Aligned/NCDC2105.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2105.sam -o 5-COVID-Aligned/NCDC2105.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2105.sam > 6-flagstat/NCDC2105.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2105.bam > 7-Coverage/NCDC2105.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2108.1.fastq NCDC2108.2.fastq 1-Trimmomatic/NCDC2108.1_paired.fastq 1-Trimmomatic/NCDC2108.1_unpaired.fastq 1-Trimmomatic/NCDC2108.2_paired.fastq 1-Trimmomatic/NCDC2108.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2108.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2108.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2108.1_paired.fastq -2 1-Trimmomatic/NCDC2108.2_paired.fastq -S 3-Human-Aligned/NCDC2108.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2108_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2108.sam -o 3-Human-Aligned/NCDC2108.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2108.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2108.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2108.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2108.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2108.bam -fq 4-Human-Unaligned/NCDC2108_1.fq -fq2 4-Human-Unaligned/NCDC2108_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2108_1.fq 4-Human-Unaligned/NCDC2108_2.fq > 5-COVID-Aligned/NCDC2108.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2108.sam -o 5-COVID-Aligned/NCDC2108.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2108.sam > 6-flagstat/NCDC2108.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2108.bam > 7-Coverage/NCDC2108.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2240_S1.1.fastq NCDC2240_S1.2.fastq 1-Trimmomatic/NCDC2240_S1.1_paired.fastq 1-Trimmomatic/NCDC2240_S1.1_unpaired.fastq 1-Trimmomatic/NCDC2240_S1.2_paired.fastq 1-Trimmomatic/NCDC2240_S1.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2240_S1.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2240_S1.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2240_S1.1_paired.fastq -2 1-Trimmomatic/NCDC2240_S1.2_paired.fastq -S 3-Human-Aligned/NCDC2240.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2240_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2240.sam -o 3-Human-Aligned/NCDC2240.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2240.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2240.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2240.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2240.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2240.bam -fq 4-Human-Unaligned/NCDC2240_1.fq -fq2 4-Human-Unaligned/NCDC2240_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2240_1.fq 4-Human-Unaligned/NCDC2240_2.fq > 5-COVID-Aligned/NCDC2240.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2240.sam -o 5-COVID-Aligned/NCDC2240.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2240.sam > 6-flagstat/NCDC2240.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2240.bam > 7-Coverage/NCDC2240.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2245_S2.1.fastq NCDC2245_S2.2.fastq 1-Trimmomatic/NCDC2245_S2.1_paired.fastq 1-Trimmomatic/NCDC2245_S2.1_unpaired.fastq 1-Trimmomatic/NCDC2245_S2.2_paired.fastq 1-Trimmomatic/NCDC2245_S2.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2245_S2.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2245_S2.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2245_S2.1_paired.fastq -2 1-Trimmomatic/NCDC2245_S2.2_paired.fastq -S 3-Human-Aligned/NCDC2245.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2245_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2245.sam -o 3-Human-Aligned/NCDC2245.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2245.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2245.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2245.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2245.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2245.bam -fq 4-Human-Unaligned/NCDC2245_1.fq -fq2 4-Human-Unaligned/NCDC2245_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2245_1.fq 4-Human-Unaligned/NCDC2245_2.fq > 5-COVID-Aligned/NCDC2245.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2245.sam -o 5-COVID-Aligned/NCDC2245.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2245.sam > 6-flagstat/NCDC2245.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2245.bam > 7-Coverage/NCDC2245.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2250_S3.1.fastq NCDC2250_S3.2.fastq 1-Trimmomatic/NCDC2250_S3.1_paired.fastq 1-Trimmomatic/NCDC2250_S3.1_unpaired.fastq 1-Trimmomatic/NCDC2250_S3.2_paired.fastq 1-Trimmomatic/NCDC2250_S3.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2250_S3.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2250_S3.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2250_S3.1_paired.fastq -2 1-Trimmomatic/NCDC2250_S3.2_paired.fastq -S 3-Human-Aligned/NCDC2250.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2250_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2250.sam -o 3-Human-Aligned/NCDC2250.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2250.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2250.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2250.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2250.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2250.bam -fq 4-Human-Unaligned/NCDC2250_1.fq -fq2 4-Human-Unaligned/NCDC2250_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2250_1.fq 4-Human-Unaligned/NCDC2250_2.fq > 5-COVID-Aligned/NCDC2250.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2250.sam -o 5-COVID-Aligned/NCDC2250.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2250.sam > 6-flagstat/NCDC2250.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2250.bam > 7-Coverage/NCDC2250.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC2251_S4.1.fastq NCDC2251_S4.2.fastq 1-Trimmomatic/NCDC2251_S4.1_paired.fastq 1-Trimmomatic/NCDC2251_S4.1_unpaired.fastq 1-Trimmomatic/NCDC2251_S4.2_paired.fastq 1-Trimmomatic/NCDC2251_S4.2_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC2251_S4.1_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC2251_S4.2_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC2251_S4.1_paired.fastq -2 1-Trimmomatic/NCDC2251_S4.2_paired.fastq -S 3-Human-Aligned/NCDC2251.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC2251_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC2251.sam -o 3-Human-Aligned/NCDC2251.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC2251.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC2251.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC2251.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC2251.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC2251.bam -fq 4-Human-Unaligned/NCDC2251_1.fq -fq2 4-Human-Unaligned/NCDC2251_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC2251_1.fq 4-Human-Unaligned/NCDC2251_2.fq > 5-COVID-Aligned/NCDC2251.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC2251.sam -o 5-COVID-Aligned/NCDC2251.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC2251.sam > 6-flagstat/NCDC2251.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC2251.bam > 7-Coverage/NCDC2251.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1257_S6_L001_R1_001.fastq NCDC1257_S6_L001_R2_001.fastq 1-Trimmomatic/NCDC1257_S6_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1257_S6_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1257_S6_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1257_S6_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1257_S6_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1257_S6_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1257_S6_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1257_S6_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1257.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1257_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1257.sam -o 3-Human-Aligned/NCDC1257.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1257.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1257.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1257.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1257.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1257.bam -fq 4-Human-Unaligned/NCDC1257_1.fq -fq2 4-Human-Unaligned/NCDC1257_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1257_1.fq 4-Human-Unaligned/NCDC1257_2.fq > 5-COVID-Aligned/NCDC1257.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1257.sam -o 5-COVID-Aligned/NCDC1257.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1257.sam > 6-flagstat/NCDC1257.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1257.bam > 7-Coverage/NCDC1257.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1441_S1_L001_R1_001.fastq NCDC1441_S1_L001_R2_001.fastq 1-Trimmomatic/NCDC1441_S1_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1441_S1_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1441_S1_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1441_S1_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1441_S1_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1441_S1_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1441_S1_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1441_S1_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1441.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1441_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1441.sam -o 3-Human-Aligned/NCDC1441.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1441.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1441.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1441.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1441.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1441.bam -fq 4-Human-Unaligned/NCDC1441_1.fq -fq2 4-Human-Unaligned/NCDC1441_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1441_1.fq 4-Human-Unaligned/NCDC1441_2.fq > 5-COVID-Aligned/NCDC1441.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1441.sam -o 5-COVID-Aligned/NCDC1441.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1441.sam > 6-flagstat/NCDC1441.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1441.bam > 7-Coverage/NCDC1441.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1444_S2_L001_R1_001.fastq NCDC1444_S2_L001_R2_001.fastq 1-Trimmomatic/NCDC1444_S2_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1444_S2_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1444_S2_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1444_S2_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1444_S2_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1444_S2_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1444_S2_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1444_S2_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1444.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1444_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1444.sam -o 3-Human-Aligned/NCDC1444.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1444.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1444.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1444.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1444.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1444.bam -fq 4-Human-Unaligned/NCDC1444_1.fq -fq2 4-Human-Unaligned/NCDC1444_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1444_1.fq 4-Human-Unaligned/NCDC1444_2.fq > 5-COVID-Aligned/NCDC1444.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1444.sam -o 5-COVID-Aligned/NCDC1444.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1444.sam > 6-flagstat/NCDC1444.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1444.bam > 7-Coverage/NCDC1444.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1604_S3_L001_R1_001.fastq NCDC1604_S3_L001_R2_001.fastq 1-Trimmomatic/NCDC1604_S3_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1604_S3_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1604_S3_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1604_S3_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1604_S3_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1604_S3_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1604_S3_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1604_S3_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1604.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1604_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1604.sam -o 3-Human-Aligned/NCDC1604.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1604.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1604.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1604.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1604.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1604.bam -fq 4-Human-Unaligned/NCDC1604_1.fq -fq2 4-Human-Unaligned/NCDC1604_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1604_1.fq 4-Human-Unaligned/NCDC1604_2.fq > 5-COVID-Aligned/NCDC1604.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1604.sam -o 5-COVID-Aligned/NCDC1604.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1604.sam > 6-flagstat/NCDC1604.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1604.bam > 7-Coverage/NCDC1604.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1614_S4_L001_R1_001.fastq NCDC1614_S4_L001_R2_001.fastq 1-Trimmomatic/NCDC1614_S4_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1614_S4_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1614_S4_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1614_S4_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1614_S4_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1614_S4_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1614_S4_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1614_S4_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1614.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1614_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1614.sam -o 3-Human-Aligned/NCDC1614.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1614.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1614.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1614.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1614.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1614.bam -fq 4-Human-Unaligned/NCDC1614_1.fq -fq2 4-Human-Unaligned/NCDC1614_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1614_1.fq 4-Human-Unaligned/NCDC1614_2.fq > 5-COVID-Aligned/NCDC1614.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1614.sam -o 5-COVID-Aligned/NCDC1614.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1614.sam > 6-flagstat/NCDC1614.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1614.bam > 7-Coverage/NCDC1614.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  NCDC1744_S5_L001_R1_001.fastq NCDC1744_S5_L001_R2_001.fastq 1-Trimmomatic/NCDC1744_S5_L001_R1_001_paired.fastq 1-Trimmomatic/NCDC1744_S5_L001_R1_001_unpaired.fastq 1-Trimmomatic/NCDC1744_S5_L001_R2_001_paired.fastq 1-Trimmomatic/NCDC1744_S5_L001_R2_001_unpaired.fastq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/NCDC1744_S5_L001_R1_001_paired.fastq -o 2-fastqc/
fastqc 1-Trimmomatic/NCDC1744_S5_L001_R2_001_paired.fastq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/NCDC1744_S5_L001_R1_001_paired.fastq -2 1-Trimmomatic/NCDC1744_S5_L001_R2_001_paired.fastq -S 3-Human-Aligned/NCDC1744.sam -p 16 --dta-cufflinks --summary-file 0-logs/NCDC1744_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/NCDC1744.sam -o 3-Human-Aligned/NCDC1744.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/NCDC1744.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/NCDC1744.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/NCDC1744.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/NCDC1744.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/NCDC1744.bam -fq 4-Human-Unaligned/NCDC1744_1.fq -fq2 4-Human-Unaligned/NCDC1744_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/NCDC1744_1.fq 4-Human-Unaligned/NCDC1744_2.fq > 5-COVID-Aligned/NCDC1744.sam
samtools sort -@ 8 5-COVID-Aligned/NCDC1744.sam -o 5-COVID-Aligned/NCDC1744.bam -O BAM
samtools flagstat 5-COVID-Aligned/NCDC1744.sam > 6-flagstat/NCDC1744.stats
genomeCoverageBed -ibam 5-COVID-Aligned/NCDC1744.bam > 7-Coverage/NCDC1744.txt
