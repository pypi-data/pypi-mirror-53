sbio
======
Collection of simple Bioinformatic tools.

fastq_quality
------
Script usage:  
`fastq_quality.py -r1 *R1*.fastq.gz -r2 *R2*.fastq.gz`  
`fastq_quality.py -h`

Module usage:  
`from sbio.fastq_quality import FASTQ_Quality`  
`fq = FASTQ_Quality(read1, read2, sampling_number)`  
`fq.run()`  

Files must be .gz zipped  
Paired reads must contain _R1 or _R2 in file name  

Along with the FASTQ file and sample name 5 FASTQ attributes are obtained:
>file_size --> FASTQ file size (human readable)
>total_read_count --> Total read count within each FASTQ file  
>sampling_size  --> Random analyzed read count  
>length_mean --> Average read length  
>read_average --> Average read quality  
>reads_gt_q30 --> Read counts with an average quality greater than 30  

Note: when calculating percent of reads above Q30 use reads_gt_q30/sampling_size  

After ran object will contain nested dot notation for each read, fq.read1.fastq --> 'sample_S25_L001_R1.fastq.gz'
