samtools index 5-COVID-Aligned/wuhan1.bam 5-COVID-Aligned/wuhan1.bam.bai
python ../../../tools/reditools2.0/src/cineca/reditools.py -f 5-COVID-Aligned/wuhan1.bam -S -s 0 -os 4 -r ../../Datasets/NC_045512.2/NC_045512.2.fa -m ../../../output/REDItools2/homopolymers_NC_045512.2.txt -c ../../../output/REDItools2/homopolymers_NC_045512.2.txt -q 33 -bq 30 -mbp 15 -Mbp 15 -o ../../../output/REDItools2/Wuhan-Editing-Paper-PRJNA601736/wuhan1.txt

samtools index 5-COVID-Aligned/wuhan2.bam 5-COVID-Aligned/wuhan2.bam.bai
python ../../../tools/reditools2.0/src/cineca/reditools.py -f 5-COVID-Aligned/wuhan2.bam -S -s 0 -os 4 -r ../../Datasets/NC_045512.2/NC_045512.2.fa -m ../../../output/REDItools2/homopolymers_NC_045512.2.txt -c ../../../output/REDItools2/homopolymers_NC_045512.2.txt -q 33 -bq 30 -mbp 15 -Mbp 15 -o ../../../output/REDItools2/Wuhan-Editing-Paper-PRJNA601736/wuhan2.txt
