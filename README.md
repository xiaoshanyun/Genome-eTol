Introduction
============
##### Genome-eTol is a software package, written in Python3 and R language, that contains the whole process to build an eTol with marker genomic sequences which include best species selection among taxa, marker genomic sequences identification and selection, orthologs selection and final eTol built. This software package aids in the construction of genomic sequence-based phylogenomic datasets. In addition, Genome-eTol currently includes a manually curated starting dataset of 100 genomic sequences families from all eukaryotic highest taxa in NCBI category representing the full breadth of known diversity in the eukaryotic tree of life. The combination of all of the foregoing features makes Genome-eTol a broadly-useful, user-friendly software tool for sophisticated phylogenomic analyses of eukaryotes.

#### Genome-eTol is constructed by four main parts:
* ##### Similarity_order | Score the similarity between alphaproteobacterial genome and eukaryote genome
* ##### Genome_sequences_extract | Extract amino acid sequences from genome
* ##### Genome_sequences_family_selection | Select suitable amino acid sequences families
* ##### Marker_sequences_selection | Select orthologs from genomic amino acid sequences families

Flow charts
===========
* ##### Similarity_order:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Similarity_order.tiff" width="140px">

* ##### Genome_sequences_extract:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Genome_sequences_extract.tiff" width="300px">

* ##### Genome_sequences_family_selection:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Genome_sequences_family_selection.tiff" width="220px">

* ##### Marker_sequences_selection:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Marker_sequences_selection.tiff" width="370px">

Test you can run Genome-eTol: python Genome-eTol.py -h

## Command line options

### Options for starting an analysis
**-e** \<dir\>: Start analysis from directory of FASTA files  
**-b** \<dir\>: Start analysis from BLAST results in OrthoFinder directory  
**-cl** \<dir1\> **-f** \<dir2\>: Start analysis from BLAST results in OrthoFinder dir1 and add FASTA files from dir2  
**-c** \<dir\>: Start analysis from orthogroups OrthoFinder directory  
**-s** \<dir\>: Start analysis from gene trees in OrthoFinder directory
 
### Options for keeping the processing data 
**-k**: Stop after preparing input files for all-vs-all sequence search (e.g. BLAST/DIAMOND)  
