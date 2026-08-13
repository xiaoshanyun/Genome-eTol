library(ape)
library(readxl)
library(treeio)
library(ggtree)
library(writexl)
library(stringr)


script_file_path <- rstudioapi::getSourceEditorContext()$path
script_dir <- dirname(script_file_path)
setwd(script_dir)

input_path_0 <- script_dir
input_path <- file.path(input_path_0, "last")
output_path_1 <- file.path(input_path, "continue")
output_path_2 <- file.path(input_path, "select")
tre_files <- list.files(path = input_path, pattern = "\\.txt$", full.names = TRUE)

i=0
j=0
for (file in tre_files){
  file_name <- tools::file_path_sans_ext(basename(file))
  txt_file_1 <- file.path(output_path_1, paste0(file_name, ".txt"))
  txt_file_2 <- file.path(output_path_2, paste0(file_name, ".txt"))
  print(file_name)
  if(file.info(file)$size>0){
  A <- read.table(file)
  A_class = A
  A_class[c('first_3')] <- substr(A_class[,1],1,3)
  colnames(A_class)[1] <- "label"
  A_bac_0 = A_class[A_class$first_3 =="bac",]
  A_bac = data.frame(A_bac_0$label)
  colnames(A_bac)<- "label"
  A_GCAF_0 = A_class[A_class$first_3 !="bac",]
  A_GCAF_1 = A_GCAF_0$label
  A_GCAF = unlist(A_GCAF_0$label)
  i = 1}
  file1 = paste(file,"t100", sep = "", collapse=NULL)
  if(file.info(file1)$size>0){
  B <- read.table(file1)
  B_class = B
  B_class[c('first_3')] <- substr(B_class[,1],1,3)
  colnames(B_class)[1] <- "label"
  B_bac_0 = B_class[B_class$first_3 =="bac",]
  B_bac = data.frame(B_bac_0$label)
  colnames(B_bac)<- "label"
  B_GCAF_0 = B_class[B_class$first_3 !="bac",]
  B_GCAF_1 = B_GCAF_0$label
  B_GCAF = unlist(B_GCAF_1)
  j = 1}
  if (1+j==2){
  C_bac = merge(A_bac, B_bac,by = "label",all = FALSE)
  C_GCAF_0 = setdiff(B_GCAF, A_GCAF)
  }
  else{C_bac=list()
  C_GCAF_0=B_GCAF}
  C_GCAF = data.frame(unique(C_GCAF_0))
  colnames(C_GCAF)<- "label"
  C = rbind(C_bac,C_GCAF)
  D <- data.frame(C)
  if (nrow(C_bac)>0){
  write.table (C, txt_file_1,row.names = FALSE,col.names =FALSE,quote = FALSE)
  }else{
    write.table (C, txt_file_2,row.names = FALSE,col.names =FALSE,quote = FALSE)
  }
}
 