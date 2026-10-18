Genome-eToL  
============
## Introduction
### Why use Genome-eToL?
Thanks to the large amount of identified mitochondrial marker proteins and new developed phylogenetic models, the eukaryote Tree of Life (eToL) can dissect the relationship among all known eukaryotic supergroups. Meantime protein eToL faces major challenges to limited sampling and LECA’s ancestral state reconstruction. Also, there is a need to develop more scientific guidance to select most ancestral taxa in each group. Moreover, rather than analyzing evolve distance with other evidence (fossils, phenotypes etc.) in protein eToL only, one more intuitive method especially genomic method is required to adequately build the eukaryotic genome evolution timeline.
&nbsp;
### Main features:  
* **Full sampling:** Only genome sequences are needed to evaluate genomic similarity to LECA.
* **Genome similarity evaluation:** A scoring procedure to estimate the genomic similarity to LECA.
* **Most LECA genomic similar taxa selection:** Supporting most genomic similar taxa selection by ranking genomic similarity in their groups.
* **Probable contaminants or LGTs removal:** An R to remove probable contaminants or LGTs to Archaea and bacteria except alphaproteobacteria.
* **Similar genomic sequences extraction:** Based on given site file, it supports similar genomic sequences extraction from genomes.
&nbsp;
## Command-line options
Test you can run Genome-eTol: `python Genome-eTol.py -h` or  `python Genome-eTol.py --help`
&nbsp;
* #### Similar genomic sequences extraction in both DNA and Amino Acid forms

  **Usage:** `python Genome-eTol.py e -c <dir> -g <dir> -s bac/euk -o <dir> (-k)` or `python Genome-eTol.py e --coord <dir> --genome <dir> --specie bac/euk --output <dir> (--keep)`
  
  **-c** \<dir\> or **--coord** \<dir\> : Input coord path; ExampleData = ExampleData/coord   
  **-g** \<dir\> or **--genome** \<dir\> : Input bacterias/eukaryotes genome path; ExampleData1 = ExampleData/genome-bac, ExampleData2 = ExampleData/genome-euk   
  **-s** bac/euk or **--specie** bac/euk : \'bac\' or \'euk\'; Write in \'bac\' if specie is bacteria, write in \'euk\' if specie is eukaryote   
  **-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result
&nbsp;
* #### Initiative marker genomic sequences dataset building

  **Usage:** `python Genome-eTol.py b -i <dir> -o <dir> (-k)` or `python Genome-eTol.py b --input <dir> --output <dir> (--keep)`
  
  **-i** \<dir\> or **--input** \<dir\> : Input excel file path; ExampleData = ExampleData/input-b
  **-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result
&nbsp;
* #### Partial sequences combination and overlapped sequences deletion
  * Step1

    **Usage:** `python Genome-eTol.py cl -i <dir> -o <dir> (-k)` or `python Genome-eTol.py cl --input <dir> --output <dir> (--keep)`
    
    **-i** \<dir\> or **--input** \<dir\> : Input fasta file path; ExampleData = ExampleData/input-cl   
    **-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result
  * step2

    **Usage:** `python Genome-eTol.py c -i1 <dir> -i2 <dir> -o <dir> (-k)` or `python Genome-eTol.py c --input1 <dir> --input2 <dir> --output <dir> (--keep)`
    
    **-i1** \<dir\> or **--input1** \<dir\> : Input sequences file path; ExampleData = ExampleData/input-cl   
    **-i2** \<dir\> or **--input2** \<dir\> :Input path which contains delete and combine folders, two folder names must be \'delete\' and \'combine\', file filename extension must be \'fasta\'; ExampleData = ExampleData/input-c   
    **-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result
&nbsp;
* #### Genome similarity evaluation

  **Usage:** `python Genome-eTol.py s -i <dir> -o <dir> (-k)` or `python Genome-eTol.py s --input <dir> --output <dir> (--keep)`
  
  **-i** \<dir\> or **--input** \<dir\> : Input coord file path; ExampleData = ExampleData/input-s   
  **-o** \<dir\> or **--output** \<dir\> : Output path; For example: Genome-eTol_result

* #### Other option: keeping the processing data
  **Usage:** **-k** or **--keep**: Keep the processing files   
##
