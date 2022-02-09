#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
folder = args[1]

setwd(folder)
# print(folder)

filenames <- list.files(pattern = "sim_number*")

test<- unlist(strsplit(folder,'/'))
prefix <- tail(test,n=2)
savefilename <- paste0(prefix[1],"_",prefix[2],".csv",sep="")
print(savefilename)
library(dplyr)
library(readr)


summary <- tibble()
secondary_infections <- tibble()
i <- 1
for(file in filenames){
  sim <- read_csv(file)
  sim <- sim %>% mutate(symptomatic = as.factor(symptomatic),bracket= cut(age,breaks = c(seq(0,80,by =5),Inf),include.lowest=TRUE,right = FALSE),day = floor(time_symptoms)) %>% group_by(day,bracket,symptomatic,infection_number) %>% summarise(n = n()) %>% mutate(sim = i)
  summary <-bind_rows(sim,summary)
  i <- i +1

}

write_csv(summary,savefilename)