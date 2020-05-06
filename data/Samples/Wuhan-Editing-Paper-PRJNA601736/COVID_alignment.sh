java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  4-Human-Unaligned/wuhan1_1.fq.1 4-Human-Unaligned/wuhan1_2.fq.1 1-Trimmomatic/wuhan1_1_paired.fq 1-Trimmomatic/wuhan1_1_unpaired.fq 1-Trimmomatic/wuhan1_2_paired.fq 1-Trimmomatic/wuhan1_2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/wuhan1_1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/wuhan1_2_paired.fq -o 2-fastqc/
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 1-Trimmomatic/wuhan1_1_paired.fq 1-Trimmomatic/wuhan1_2_paired.fq > 5-COVID-Aligned/wuhan1.sam
samtools sort -@ 8 5-COVID-Aligned/wuhan1.sam -o 5-COVID-Aligned/wuhan1.bam -O BAM
samtools flagstat 5-COVID-Aligned/wuhan1.sam > 6-flagstat/wuhan1.stats
genomeCoverageBed -ibam 5-COVID-Aligned/wuhan1.bam > 7-Coverage/wuhan1.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  4-Human-Unaligned/wuhan2_1.fq.1 4-Human-Unaligned/wuhan2_2.fq.1 1-Trimmomatic/wuhan2_1_paired.fq 1-Trimmomatic/wuhan2_1_unpaired.fq 1-Trimmomatic/wuhan2_2_paired.fq 1-Trimmomatic/wuhan2_2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/wuhan2_1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/wuhan2_2_paired.fq -o 2-fastqc/
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 1-Trimmomatic/wuhan2_1_paired.fq 1-Trimmomatic/wuhan2_2_paired.fq > 5-COVID-Aligned/wuhan2.sam
samtools sort -@ 8 5-COVID-Aligned/wuhan2.sam -o 5-COVID-Aligned/wuhan2.bam -O BAM
samtools flagstat 5-COVID-Aligned/wuhan2.sam > 6-flagstat/wuhan2.stats
genomeCoverageBed -ibam 5-COVID-Aligned/wuhan2.bam > 7-Coverage/wuhan2.txt
