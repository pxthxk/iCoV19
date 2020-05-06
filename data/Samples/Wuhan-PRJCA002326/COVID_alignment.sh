java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  CRR119894_f1.fq CRR119894_r2.fq 1-Trimmomatic/CRR119894_f1_paired.fq 1-Trimmomatic/CRR119894_f1_unpaired.fq 1-Trimmomatic/CRR119894_r2_paired.fq 1-Trimmomatic/CRR119894_r2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/CRR119894_f1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/CRR119894_r2_paired.fq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/CRR119894_f1_paired.fq -2 1-Trimmomatic/CRR119894_r2_paired.fq -S 3-Human-Aligned/CRR119894.sam -p 16 --dta-cufflinks --summary-file 0-logs/CRR119894_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/CRR119894.sam -o 3-Human-Aligned/CRR119894.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/CRR119894.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/CRR119894.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/CRR119894.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/CRR119894.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/CRR119894.bam -fq 4-Human-Unaligned/CRR119894_1.fq -fq2 4-Human-Unaligned/CRR119894_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/CRR119894_1.fq 4-Human-Unaligned/CRR119894_2.fq > 5-COVID-Aligned/CRR119894.sam
samtools sort -@ 8 5-COVID-Aligned/CRR119894.sam -o 5-COVID-Aligned/CRR119894.bam -O BAM
samtools flagstat 5-COVID-Aligned/CRR119894.sam > 6-flagstat/CRR119894.stats
genomeCoverageBed -ibam 5-COVID-Aligned/CRR119894.bam > 7-Coverage/CRR119894.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  CRR119895_f1.fq CRR119895_r2.fq 1-Trimmomatic/CRR119895_f1_paired.fq 1-Trimmomatic/CRR119895_f1_unpaired.fq 1-Trimmomatic/CRR119895_r2_paired.fq 1-Trimmomatic/CRR119895_r2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/CRR119895_f1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/CRR119895_r2_paired.fq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/CRR119895_f1_paired.fq -2 1-Trimmomatic/CRR119895_r2_paired.fq -S 3-Human-Aligned/CRR119895.sam -p 16 --dta-cufflinks --summary-file 0-logs/CRR119895_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/CRR119895.sam -o 3-Human-Aligned/CRR119895.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/CRR119895.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/CRR119895.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/CRR119895.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/CRR119895.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/CRR119895.bam -fq 4-Human-Unaligned/CRR119895_1.fq -fq2 4-Human-Unaligned/CRR119895_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/CRR119895_1.fq 4-Human-Unaligned/CRR119895_2.fq > 5-COVID-Aligned/CRR119895.sam
samtools sort -@ 8 5-COVID-Aligned/CRR119895.sam -o 5-COVID-Aligned/CRR119895.bam -O BAM
samtools flagstat 5-COVID-Aligned/CRR119895.sam > 6-flagstat/CRR119895.stats
genomeCoverageBed -ibam 5-COVID-Aligned/CRR119895.bam > 7-Coverage/CRR119895.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  CRR119896_f1.fq CRR119896_r2.fq 1-Trimmomatic/CRR119896_f1_paired.fq 1-Trimmomatic/CRR119896_f1_unpaired.fq 1-Trimmomatic/CRR119896_r2_paired.fq 1-Trimmomatic/CRR119896_r2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/CRR119896_f1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/CRR119896_r2_paired.fq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/CRR119896_f1_paired.fq -2 1-Trimmomatic/CRR119896_r2_paired.fq -S 3-Human-Aligned/CRR119896.sam -p 16 --dta-cufflinks --summary-file 0-logs/CRR119896_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/CRR119896.sam -o 3-Human-Aligned/CRR119896.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/CRR119896.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/CRR119896.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/CRR119896.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/CRR119896.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/CRR119896.bam -fq 4-Human-Unaligned/CRR119896_1.fq -fq2 4-Human-Unaligned/CRR119896_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/CRR119896_1.fq 4-Human-Unaligned/CRR119896_2.fq > 5-COVID-Aligned/CRR119896.sam
samtools sort -@ 8 5-COVID-Aligned/CRR119896.sam -o 5-COVID-Aligned/CRR119896.bam -O BAM
samtools flagstat 5-COVID-Aligned/CRR119896.sam > 6-flagstat/CRR119896.stats
genomeCoverageBed -ibam 5-COVID-Aligned/CRR119896.bam > 7-Coverage/CRR119896.txt

java -jar /tahseen/software/Trimmomatic-0.39/trimmomatic-0.39.jar PE  CRR119897_f1.fq CRR119897_r2.fq 1-Trimmomatic/CRR119897_f1_paired.fq 1-Trimmomatic/CRR119897_f1_unpaired.fq 1-Trimmomatic/CRR119897_r2_paired.fq 1-Trimmomatic/CRR119897_r2_unpaired.fq ILLUMINACLIP:/tahseen/software/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:100
fastqc 1-Trimmomatic/CRR119897_f1_paired.fq -o 2-fastqc/
fastqc 1-Trimmomatic/CRR119897_r2_paired.fq -o 2-fastqc/
hisat2 -x ../../Datasets/GRCh37-Assembly/GRCh37.primary_assembly.genome -1 1-Trimmomatic/CRR119897_f1_paired.fq -2 1-Trimmomatic/CRR119897_r2_paired.fq -S 3-Human-Aligned/CRR119897.sam -p 16 --dta-cufflinks --summary-file 0-logs/CRR119897_Human_Aligned.log
samtools sort -@ 8 3-Human-Aligned/CRR119897.sam -o 3-Human-Aligned/CRR119897.bam -O BAM
samtools view -u -f 4 -F 264 3-Human-Aligned/CRR119897.bam > 4-Human-Unaligned/temp1.bam
samtools view -u -f 8 -F 260 3-Human-Aligned/CRR119897.bam > 4-Human-Unaligned/temp2.bam
samtools view -u -f 12 -F 256 3-Human-Aligned/CRR119897.bam > 4-Human-Unaligned/temp3.bam
samtools merge -u - 4-Human-Unaligned/temp[123].bam | samtools sort -n -o 4-Human-Unaligned/CRR119897.bam
rm 4-Human-Unaligned/temp1.bam 4-Human-Unaligned/temp2.bam 4-Human-Unaligned/temp3.bam
bamToFastq -i 4-Human-Unaligned/CRR119897.bam -fq 4-Human-Unaligned/CRR119897_1.fq -fq2 4-Human-Unaligned/CRR119897_2.fq
bwa mem ../../Datasets/NC_045512.2/NC_045512.2.fa 4-Human-Unaligned/CRR119897_1.fq 4-Human-Unaligned/CRR119897_2.fq > 5-COVID-Aligned/CRR119897.sam
samtools sort -@ 8 5-COVID-Aligned/CRR119897.sam -o 5-COVID-Aligned/CRR119897.bam -O BAM
samtools flagstat 5-COVID-Aligned/CRR119897.sam > 6-flagstat/CRR119897.stats
genomeCoverageBed -ibam 5-COVID-Aligned/CRR119897.bam > 7-Coverage/CRR119897.txt
