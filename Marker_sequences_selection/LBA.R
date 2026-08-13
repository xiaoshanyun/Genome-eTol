library(ape)
library(treeio)
library(ggtree)
library(writexl)
library(stringr)


script_file_path <- rstudioapi::getSourceEditorContext()$path
script_dir <- dirname(script_file_path)
setwd(script_dir)

input_path_0 <- script_dir
input_path <- file.path(input_path_0, "input-LBA")
output_path <-  file.path(input_path_0, "LBA-result")
if (!dir.exists(output_path)) {
  dir.create(output_path)
} else {
  print("Dir already exists!")
}
tre_files <- list.files(path = input_path, pattern = "\\.tre$", full.names = TRUE)

for (file in tre_files){
  tree <- read.tree(file)
  file_name <- tools::file_path_sans_ext(basename(file))
  txt_file <- file.path(output_path, paste0(file_name, ".txt"))
  as.phylo(tree)
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
  distance = as.vector(as.matrix(t(distances)))
  distance = data.frame(distance)
  result <- cbind(result_x,result_y)
  df = cbind(result,distance)
  df <- df[df[, 3] != -1, ]
  id_list = data.frame()
  id_list = data.frame(t(t(df[!duplicated(df$result_x),][,1])))
  colnames(id_list)[1] <- "name"
  rownames(id_list) <- NULL
  id_list[,'mean'] <- NA
  df <- df[order(-df$distance), ]
  mean_list = data.frame()
  for (j in 1:nrow(id_list)){
    id = id_list[j,1]
    id_frame = df[df[, 1] %in%id, ][1:5,]
    mean_distance <- mean(id_frame$distance, na.rm = TRUE)
    id_list[j,2] = mean_distance
  }
  percent25 <- quantile(id_list$mean, probs = 0.25)
  percent75 <- quantile(id_list$mean, probs = 0.75)
  limit = 3*(percent75-percent25)+percent75
  delete_frame = data.frame(id_list[id_list[, 2] > limit,])
  colnames(delete_frame)[1] <- "name"
  delete_id = t(t(delete_frame$name))
  write.table (delete_id, txt_file,row.names = FALSE,col.names =FALSE,quote = FALSE)
}
