Remove the possible contaminants and lateral gene transfers (LGTs) pollutions in phylogenetic trees.

========================

Introduction

    These files are coding by R language. Please open them with RStudio.

    boostrap_t100.R and boostrap_b1000.R are the tools to find the possible LGT pollutions among the eukaryote sequences.

    They contains three functions. 
    1. Find the eukaryote sequences branched strongly (more than 95% UFBOOT2, more than 85% true bootstrap support) with archaeal or baterial (except alphaproteobacteria) clades.
    2. Find the eukaryote sequences which are separated from them by very short branch lengths (<0.22).
    3. Find the meaningless archaeal or baterial (except alphaproteobacteria) clades.
    Results will be in "last".

    intersect.R is the tool to get the intersection between the results from boostrap_t100.R and boostrap_b1000.R.
    intersect.R's result will be in "last/intersect" or "last/select".
    If exists possible LGT pollution in both b1000 and t100 trees with same taxon, the result will be in "last/intersect".
    Else, the result will be in "last/select".
