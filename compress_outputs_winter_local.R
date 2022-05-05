#!/usr/bin/env Rscript

# args = commandArgs(trailingOnly=TRUE)
# folder = args[1]

library(dplyr)
library(readr)

root_folder= "C:\\Users\\thaophuongl\\winter_outputs\\"

for(population_type in c("younger","older")){
  param_list_younger = seq(1,12,1)
  param_list_older = seq(13,24,1)
  if (population_type=="younger"){
  population_list = param_list_younger
  } else{
    population_list = param_list_older
  }
  
  for(paramNum in population_list){
      folder = paste0(root_folder,"abm_simulation_people_params_",paramNum,"_output_winter_sims_",population_type,"_init10")
      
      print(folder)
      setwd(folder)
      
      
      filenames_all <- list.files(pattern = "sim_number*")
      filenames_prewinter <- list.files(pattern = "*prewinter.csv")
      filenames_winter <- setdiff(filenames_all,filenames_prewinter)
      
      test<- unlist(strsplit(folder,'/'))
      prefix <- tail(test,n=2)
      #savefilename <- paste0(prefix[1],"_",prefix[2],".csv",sep="")
      savefilename <- paste0(prefix[1],".csv",sep="")
      #savefilename <- paste0(prefix[1],"_abm_ages.csv",sep="")
      print(savefilename)
      
      
      # for(file in filenames_winter){
      #   print(file)
      # }
      

      summary <- tibble()
      secondary_infections <- tibble()
      i <- 1
      for(file in filenames_winter){
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
      
    
    
  }
  
  
}


