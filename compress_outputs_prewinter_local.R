#!/usr/bin/env Rscript

# args = commandArgs(trailingOnly=TRUE)
# folder = args[1]
root_folder= "C:\\Users\\thaophuongl\\pre-winter_embryo_outputs\\"

for(population_type in c("younger","older")){
  param_list_younger = c(1,5,9)
  param_list_older = c(13,17,21)
  if (population_type=="younger"){
  population_list = param_list_younger
  } else{
    population_list = param_list_older
  }
  
  for(paramNum in population_list){
    for (simnum in c(1,2)){
      folder = paste0(root_folder,"abm_pre-simulation_parameters_",paramNum,"_output_embryo_sim_params_",simnum,"_",population_type)
      
      print(folder)
      setwd(folder)
      
      
      filenames <- list.files(pattern = "sim_number*")
      
      test<- unlist(strsplit(folder,'/'))
      prefix <- tail(test,n=2)
      #savefilename <- paste0(prefix[1],"_",prefix[2],".csv",sep="")
      #savefilename <- paste0(prefix[1],".csv",sep="")
      savefilename <- paste0(prefix[1],"_abm_ages.csv",sep="")
      print(savefilename)
      library(dplyr)
      library(readr)
      
      
      summary <- tibble()
      secondary_infections <- tibble()
      i <- 1
      for(file in filenames){
        if(file.size(file) < 1L){
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
  
  
}


