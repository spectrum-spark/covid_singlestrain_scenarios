#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
folder = args[1]

setwd(folder)
filenames <- list.files(pattern = "sim_number*")

library(dplyr)
library(readr)


summary <- tibble()
secondary_infections <- tibble()
i <- 1
for(file in filenames){
  sim <- read_csv(file)
  sim <- sim %>% mutate(symptomatic = as.factor(symptomatic),bracket= cut(age,breaks = c(seq(0,80,by =5),Inf),include.lowest=TRUE,right = FALSE),day = cut(time_symptoms,breaks = seq(0,1000,by = 1),labels = FALSE)) %>% group_by(day,bracket) %>% summarise(n = n()) %>% mutate(sim = i)
  summary <-bind_rows(sim,summary)
  i <- i +1

}

write_csv(summary,"CompressedSymptomOnset.csv")