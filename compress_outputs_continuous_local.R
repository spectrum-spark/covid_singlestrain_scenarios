#!/usr/bin/env Rscript

# args = commandArgs(trailingOnly=TRUE)
# folder = args[1]

library(dplyr)
library(readr)

# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_2_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_3_outputs\\"

#root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_first_then_cont_exposure_outputs\\"
#root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_cont_exposure_outputs_daily\\"
#root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_cont_exposure_outputs_weekly\\"

# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_outputs\\"
# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_400_outputs\\"


# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_400-2_outputs\\"
# TP_list = c("1.1","1.225","1.4","1.575")# ,"1.75")


root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs\\"
TP_list = c("0.8","0.9","1.0","1.1","1.2000000000000002","1.3","1.4","1.5","1.6")

root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_no_vax_outputs\\"



# root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs\\"
TP_list = c("0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95")


root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_no_vax_outputs\\"


#root_folder= "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs\\"
TP_list = c("0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05")


#root_folder= "C:\\Users\\thaophuongl\\covid_no_ttiq_450-2_ibm_4th_doses_newstrain_outputs\\"


for(population_type in c("older" ,"younger")){#
  #population_list = seq(1,6,1)
  #population_list = c(5)
  population_list = c(1) # for the no vax version
  # TP_list = c("1.2","1.625","2.05","2.4749999999999996","2.9")
  # TP_list = c("2.0","2.25","2.5","2.75","3.0")
  # TP_list = c("1.75","2.0","2.25","2.5","2.75")
  
  #TP_list = c("1.75","2.75")
  #population_list = c(1,6)
  
  for(paramNum in population_list){
    for(TP in TP_list){
      folder = paste0(root_folder,"abm_continuous_simulation_parameters_",population_type,"_",paramNum,"_SOCRATES_TP",TP)
      
      print(folder)
      setwd(folder)
      
      
      filenames_all <- list.files(pattern = "sim_number*")
      filenames_individuals <- list.files(pattern = "*individuals.csv")
      filenames_matlab <- list.files(pattern = "*mat")
      filenames_matlab_full <- list.files(pattern = "*dataframe.csv")
      filenames_main <- setdiff(filenames_all,c(filenames_individuals,filenames_matlab,filenames_matlab_full))
      print(filenames_main)
      
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
 

