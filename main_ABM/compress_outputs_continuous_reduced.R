#!/usr/bin/env Rscript

library(dplyr)
library(readr)

args = commandArgs(trailingOnly=TRUE)
root_folder = args[1] # paste0(root_folder,"abm_continuous_simulation_parameters_",population_type,"_",paramNum,"_SOCRATES_TP",TP)

folderpart2 = args[2] # "abm_continuous_simulation_parameters_",population_type,"_",paramNum,"_SOCRATES_TP"

TP_i = strtoi(args[3])
TP_list = c('1.05', '1.95')
TP = TP_list[TP_i]

folder = paste0(root_folder,folderpart2,TP)

print(folder)

setwd(folder)


filenames_all <- list.files(pattern = "sim_number*")
filenames_individuals <- list.files(pattern = "*individuals.csv")
filenames_matlab <- list.files(pattern = "*mat")
filenames_matlab_full <- list.files(pattern = "*dataframe.csv")
filenames_main <- setdiff(filenames_all,c(filenames_individuals,filenames_matlab,filenames_matlab_full))
print(filenames_main)
      
#test<- unlist(strsplit(folder,'/'))
#front <- head(test,n=
#prefix <- tail(test,n=2)
#print(prefix)
#savefilename <- paste0(prefix[1],"_",prefix[2],".csv",sep="")
#savefilename <- paste0("/../",prefix[2],".csv",sep="")
#savefilename <- paste0(prefix[1],".csv",sep="")
#savefilename <- paste0(prefix[1],"_abm_ages.csv",sep="")

#savefilename <- paste0(folder,".csv",sep="")
savefilename <- paste0("../",folderpart2,TP,".csv",sep="") 
print(savefilename)


summary <- tibble()
secondary_infections <- tibble()
i <- 1
for(file in filenames_main){
        if(file.size(file) == 0L){
          print("EMPTY!")
        }
        else{
          sim <- read_csv(file)
          #sim <- sim %>% mutate(symptomatic = as.factor(symptomatic),bracket= cut(age,breaks = c(seq(0,80,by =5),Inf),include.lowest=TRUE,right = FALSE),day = floor(time_symptoms),vaccine = as.factor(vaccine)) %>% group_by(day,bracket,symptomatic,infection_number,vaccine) %>% summarise(n = n()) %>% mutate(sim = i)
          sim <- sim %>% mutate(symptomatic = as.factor(symptomatic),bracket= cut(age,breaks = c(0,5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80,Inf),include.lowest=TRUE,right = FALSE),day = floor(time_symptoms),vaccine = as.factor(vaccine)) %>% group_by(day,bracket,symptomatic,infection_number,vaccine) %>% summarise(n = n()) %>% mutate(sim = i)

          summary <-bind_rows(sim,summary)

        }
        i <- i +1


}

write_csv(summary,savefilename)
      
 

