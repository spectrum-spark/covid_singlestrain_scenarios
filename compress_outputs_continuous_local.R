#!/usr/bin/env Rscript

# args = commandArgs(trailingOnly=TRUE)
# folder = args[1]

library(dplyr)
library(readr)

# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_2_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_3_outputs\\"

root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_first_then_cont_exposure_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_cont_exposure_outputs_daily\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_cont_exposure_outputs_weekly\\"


for(population_type in c("younger","older")){
  population_list = seq(1,6,1)
  # TP_list = c("1.2","1.625","2.05","2.4749999999999996","2.9")
  # TP_list = c("2.0","2.25","2.5","2.75","3.0")
  TP_list = c("1.75","2.0","2.25","2.5","2.75")
  
  TP_list = c("1.75","2.75")
  population_list = c(1,6)
  
  for(paramNum in population_list){
    for(TP in TP_list){
      folder = paste0(root_folder,"abm_continuous_simulation_parameters_",population_type,"_",paramNum,"_SOCRATES_TP",TP)
      
      print(folder)
      setwd(folder)
      
      
      filenames_all <- list.files(pattern = "sim_number*")
      filenames_individuals <- list.files(pattern = "*individuals.csv")
      filenames_main <- setdiff(filenames_all,filenames_individuals)
      
      test<- unlist(strsplit(folder,'/'))
      prefix <- tail(test,n=2)
      #savefilename <- paste0(prefix[1],"_",prefix[2],".csv",sep="")
      savefilename <- paste0(prefix[1],".csv",sep="")
      #savefilename <- paste0(prefix[1],"_abm_ages.csv",sep="")
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
      
    }
    
      
      
    
    
  }
  
  
}
 

