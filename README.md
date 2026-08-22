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
* ### Similarity_order:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Similarity_order.tiff" width="140px">

* ### Genome_sequences_extract:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Genome_sequences_extract.tiff" width="300px">

* ### Genome_sequences_family_selection:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Genome_sequences_family_selection.tiff" width="220px">

* ### Marker_sequences_selection:
<img src="https://github.com/xiaoshanyun/Genome-eTol/blob/main/assets/Marker_sequences_selection.tiff" width="370px">



## Command line options
Test you can run Genome-eTol: `python Genome-eTol.py -h` or  `python Genome-eTol.py --help`

### Options for getting amino acid sequences from genome sequences

**Usage:** `python Genome-eTol.py e -c <dir> -g <dir> -s bac/euk -o <dir> (-k)` or `python Genome-eTol.py e --coord <dir> --genome <dir> --specie bac/euk --output <dir> (--keep)`   

**-c** \<dir\> or **--coord** \<dir\> : Input coord path; ExampleData = ExampleData/coord   
**-g** \<dir\> or **--genome** \<dir\> : Input bacterias/eukaryotes genome path; ExampleData1 = ExampleData/genome-bac, ExampleData2 = ExampleData/genome-euk   
**-s** bac/euk or **--specie** bac/euk : \'bac\' or \'euk\'; Write in \'bac\' if specie is bacteria, write in \'euk\' if specie is eukaryote   
**-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result   

### Options for getting amino acid sequences from genome sequences

**Usage:** `python Genome-eTol.py b -i <dir> -o <dir> (-k)` or `python Genome-eTol.py b --input <dir> --output <dir> (--keep)`   

**-i** \<dir\> or **--input** \<dir\> : Input excel file path; ExampleData = ExampleData/input-b   
**-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result   

### Options for getting a pre-list for subprocess: option `c`

**Usage:** `python Genome-eTol.py cl -i <dir> -o <dir> (-k)` or `python Genome-eTol.py cl --input <dir> --output <dir> (--keep)`   

**-i** \<dir\> or **--input** \<dir\> : Input fasta file path; ExampleData = ExampleData/input-cl   
**-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result   

### Options for combining partial sequences and deleting meaningless sequences

**Usage:** `python Genome-eTol.py c -i1 <dir> -i2 <dir> -o <dir> (-k)` or `python Genome-eTol.py c --input1 <dir> --input2 <dir> --output <dir> (--keep)`   

**-i1** \<dir\> or **--input1** \<dir\> : Input sequences file path; ExampleData = ExampleData/input-cl   
**-i2** \<dir\> or **--input2** \<dir\> :Input path which contains delete and combine folders, two folder names must be \'delete\' and \'combine\', file filename extension must be \'fasta\'; ExampleData = ExampleData/input-c   
**-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result   

### Options for scoring the similarity between two species\' genome

**Usage:** `python Genome-eTol.py s -i <dir> -o <dir> (-k)` or `python Genome-eTol.py s --input <dir> --output <dir> (--keep)`   
**-i** \<dir\> or **--input** \<dir\> : Input coord file path; ExampleData = ExampleData/input-s   
**-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result   
 
### Options for keeping the processing data 
**-k**: Keep the processing files   
