Remove the possible contaminants and lateral gene transfers (LGTs) pollutions in phylogenetic trees.

========================

Introduction

    These files are coding by R language.

    boostrap_t100.R and boostrap_b1000.R are the tools to find the possible LGT pollutions among the eukaryote sequences. 

    They contains three functions. 
    1. Find the eukaryote sequences branched strongly (more than 95% UFBOOT2, more than 85% true bootstrap support) with archaeal or baterial (except alphaproteobacteria) clades.
    2. Find the eukaryote sequences which are separated from them by very short branch lengths (<0.22).
    3. Find the meaningless archaeal or baterial (except alphaproteobacteria) clades.
