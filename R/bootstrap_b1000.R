#------------------------------------------------------------------------------------------------------------
#First part: Import packages and read Newick filesoutput_path <- file.path(input_path_0, "last")

library(ape)
library(treeio)
library(ggtree)
library(writexl)
library(stringr)


script_file_path <- rstudioapi::getSourceEditorContext()$path
script_dir <- dirname(script_file_path)
setwd(script_dir)

input_path_0 <- script_dir
input_path <- file.path(input_path_0, "input-R/b1000")
output_path <- file.path(input_path_0, "last")
output_path_1 <- file.path(output_path, "continue")
output_path_2 <- file.path(output_path, "select")

if (!dir.exists(output_path)) {
  dir.create(output_path)
  dir.create(output_path_1)
  dir.create(output_path_2)
}

tre_files <- list.files(path = input_path, pattern = "\\.tre$", full.names = TRUE)

for (file in tre_files){
  tree <- read.tree(file)
  file_name <- tools::file_path_sans_ext(basename(file))
  txt_file <- file.path(output_path, paste0(file_name, ".txt"))
  current_time_x <- Sys.time()
  as.phylo(tree)
  tree_df=ggtree::fortify(tree)
  tree_trim = tree_df[1:5]

  #------------------------------------------------------------------------------------------------------------
  #Second part: find the mito IDs which have a boostrap value greater than 85% with bacterial or archaea
  tree_trim$isTip[tree_trim$isTip != TRUE] <- 0
  df_end <- tree_trim[tree_trim[, 5] ==1, ]
  df_end[c('first_3')] <- substr(df_end$label,1,3)
  df_node <- tree_trim[tree_trim[, 5] ==0, ]
  df_node[is.na(df_node)] <- 100
  df_node <- df_node[-1,]
  df_node[c('first_3')] <- ""
  tree_trim = rbind(df_end,df_node)
  df_node <- data.frame(sapply(df_node, as.numeric))
  node_pool_unclean_0 <- df_node[df_node[, 4] >=95, ]
  node_pool_unclean = node_pool_unclean_0[complete.cases(node_pool_unclean_0[ , c(1,2)]),]
  GCA_list <- df_end[df_end[, 6] =="GCA", ]
  GCA_list_node = merge(GCA_list, node_pool_unclean,by.x = "parent", by.y = "node",all = FALSE)[,1:6]
  final_down_pool <- data.frame()
  up_node_0 <- data.frame()
  up_node <- data.frame()
  up_node_pool <- data.frame()
  if (nrow(GCA_list_node)>0){
  for (i in 1:nrow(GCA_list_node)){
    up_num_up = as.numeric(GCA_list_node[i,1])
    up_node_0 = node_pool_unclean[node_pool_unclean[, 2] ==up_num_up, ]
    while (nrow(up_node_0)>0){
      up_num = up_num_up
      up_num_up = as.numeric(up_node_0[1, 1])
      up_node_0 = node_pool_unclean[node_pool_unclean[, 2] ==up_num_up, ]
    }
    up_node_pool <- rbind(up_node_pool,up_num)
    
    uni_up_node_pool <- data.frame(up_node_pool[!duplicated(up_node_pool[,1]),])
    colnames(uni_up_node_pool)[1] <- "node"
    down_node_0 = tree_trim[tree_trim[, 1] ==up_num, ]
    GCA_node_1 = GCA_list_node[i,2]
    down_node <- down_node_0[down_node_0[,2] != GCA_node_1, ]
    final_down_pool_0 <- data.frame()
    while (nrow(down_node)>0){
      down_num = as.numeric(down_node[1, 2])
      down_thr_pool_now <- tree_trim[tree_trim[, 1] ==down_num, ]
      down_node_end_pool <- down_node[down_node[,5] =="1", ]
      down_node_pool <- down_node[-1,]
      down_node <- down_node_pool[down_node_pool[, 5] ==0, ]
      down_node <- rbind(down_node,down_thr_pool_now)
      final_down_pool_0 <- rbind(final_down_pool_0,down_node_end_pool)
    }
    final_down_pool <- rbind(final_down_pool,final_down_pool_0)
  }
  down_pool_bac <- final_down_pool[final_down_pool[, 6] =="bac", ]
  uni_num_final_pool <- down_pool_bac[!duplicated(down_pool_bac$label),]
  if (nrow(uni_num_final_pool) != 0){
    bootstrap_list = uni_num_final_pool[, 4]}else{bootstrap_list = uni_num_final_pool}
  }
  #View(bootstrap_list)

  #------------------------------------------------------------------------------------------------------------
  #Third part: find the mito IDs which have a evolve distance less than 0.22 with bacterial or archaea
  otus = unique(tree$taxa)
  distances = cophenetic(tree)
  z = colnames(distances)
  
  result_x = data.frame()
  result_x <-rep(z,each=length(z))
  result_y = data.frame()
  len = length(z)
  for (i in 1:len){
    result_y <- c(result_y,z)
  }
  
  distances[lower.tri(distances)] = -1
  distances[distances>0.22] = -2
  distance = as.vector(as.matrix(t(distances)))
  distance = data.frame(distance)
  result <- cbind(result_x,result_y)
  
  df = cbind(result,distance)
  df <- df[df[, 3] != -2, ]
  df <- df[df[, 3] != -1, ]
  df[c('First_3')] <- substr(df[, 1],1,3)
  df[c('Last_3')] <- substr(df[, 2],1,3)
  
  df$First_3 <- gsub("bac", "-1", df$First_3)
  df$First_3 <- gsub("GCA", "1", df$First_3)
  df$First_3 <- gsub("GCF", "1", df$First_3)
  df$Last_3 <- gsub("bac", "-1", df$Last_3)
  df$Last_3 <- gsub("GCA", "1", df$Last_3)
  df$Last_3 <- gsub("GCF", "1", df$Last_3)
  
  compile = df[,c(1,2,4,5)]
  count_col = compile[,c(3,4)]
  count_col <- data.frame(lapply(count_col, as.numeric))
  compile$count <- rowSums(count_col)
  compile <- compile[compile[, 5] == 0, ]
  compile <- na.omit(compile)
  
  compile_x <- compile[compile[, 3] == -1, ]
  compile_y <- compile[compile[, 3] == 1, ]
  compile_x1 <- compile_x[,c(1)]
  compile_y1 <- compile_y[,c(2)]
  compile_L <- c(compile_x1,compile_y1)
  compile_L = unique(compile_L)
  
  compile_Lt = t(compile_L)
  distance_list = data.frame(t(compile_Lt))
  colnames(distance_list) <- c("label")
  #View(distance_list)

  
  #------------------------------------------------------------------------------------------------------------
  #Forth part: find the bacterial or archaea IDs near mito IDs
  df_bac <- df_end[df_end[, 6] =="bac", ]
  df_GCA <- df_end[df_end[, 6] =="GCA", ]
  up_node_pool = data.frame()
  up_node = data.frame()
  down_node = data.frame()
  GCA_all = data.frame()
  for (i in 1:nrow(df_bac)){
    id = as.numeric(df_bac[i,1])
    up_node_pool <- tree_trim[tree_trim[, 2] ==id, ]
    down_node_pool <- tree_trim[tree_trim[,1] ==id, ]
    down_node <- down_node_pool[down_node_pool[, 6] =="GCA", ]

    for (j in 1:nrow(up_node_pool)){
      id2 = as.numeric(up_node_pool[j,1])
      up_node <- df_GCA[df_GCA[, 1] ==id2, ]
    }
    GCA = rbind(up_node,down_node)
    GCA_all = rbind(GCA_all,GCA)
  }
  GCA_all <- na.omit(GCA_all)
  GCA_list1 = GCA_all[,4]    
  GCA_list <- GCA_list1[!duplicated(GCA_list1$label),]
  #------------------------------------------------------------------------------------------------------------
  last_list2 <- rbind(bootstrap_list,distance_list)
  last_list1 <- rbind(last_list2,GCA_list)
  last_list = unique(last_list1)
  last_list = data.frame(lapply(last_list, unlist))
  #View(last_list)

  
  write.table (last_list, txt_file,row.names = FALSE,col.names =FALSE,quote = FALSE) 
}
