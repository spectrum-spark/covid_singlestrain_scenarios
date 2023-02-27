library(data.table)
library(stringr)
#Baseline scenarios:
scenarios <- c("scenario2_2000Omicron/", "scenario14_2000Omicron", "scenario25_2000Omicron_Baseline", "scenario26_2000Omicron_Baseline")


combined_scenarios <- lapply(scenarios, function(s) {
    message(glue::glue("Running scenario {s}"))
    sims <- list.files(glue::glue("/home/michaell/cm37_scratch/health/NSW_outputs/{s}"), full.names = T, pattern="*[0-9].csv")
    
    combined_sims <- lapply(1:length(sims), function(i) {
        message(glue::glue("Doing sim {i}"))
        sim_file <- fread(sims[i])

        sim_file[, age_band := paste0(floor(age/10) * 10, "-", floor(age/10)*10+9),]
        sim_file[, day_infection := floor(time_symptoms)]

        aggregated <- sim_file[, .N, by=list(age_band, day_infection, symptomatic)]
        aggregated[, PHSM := "baseline"]
        aggregated[, iteration := 1]
        aggregated[, scenario := str_extract(s, "scenario[0-9]+") ]

        return (aggregated)
    })
    
    return (rbindlist(combined_sims))
})
combined_scenarios <- rbindlist(combined_scenarios)

fwrite(combined_scenarios, "/home/michaell/cm37_scratch/health/NSW_outputs/combined_scenarios_baseline.csv")

# #Low scenarios:
# scenarios <- c("scenario2_2000Omicron_Low/", "scenario14_2000Omicron_Low", "scenario25_2000Omicron_Low", "scenario26_2000Omicron_Low")


# combined_scenarios <- lapply(scenarios, function(s) {
#     message(glue::glue("Running scenario {s}"))
#     sims <- list.files(glue::glue("/home/michaell/cm37_scratch/health/NSW_outputs/{s}"), full.names = T, pattern="*[0-9].csv")
    
#     combined_sims <- lapply(1:length(sims), function(i) {
#         message(glue::glue("Doing sim {i}"))
#         sim_file <- fread(sims[i])

#         sim_file[, age_band := paste0(floor(age/10) * 10, "-", floor(age/10)*10+9),]
#         sim_file[, day_infection := floor(time_symptoms)]

#         aggregated <- sim_file[, .N, by=list(age_band, day_infection, symptomatic)]
#         aggregated[, PHSM := "low"]
#         aggregated[, iteration := 1]
#         aggregated[, scenario := str_extract(s, "scenario[0-9]+") ]

#         return (aggregated)
#     })
    
#     return (rbindlist(combined_sims))
# })

# combined_scenarios <- rbindlist(combined_scenarios)

# fwrite(combined_scenarios, "/home/michaell/cm37_scratch/health/NSW_outputs/combined_scenarios_low.csv")

# #Medium scenarios:
# scenarios <- c("scenario2_2000Omicron_Med/", "scenario14_2000Omicron_Med", "scenario25_2000Omicron_Med", "scenario26_2000Omicron_Med")


# combined_scenarios <- lapply(scenarios, function(s) {
#     message(glue::glue("Running scenario {s}"))
#     sims <- list.files(glue::glue("/home/michaell/cm37_scratch/health/NSW_outputs/{s}"), full.names = T, pattern="*[0-9].csv")
    
#     combined_sims <- lapply(1:length(sims), function(i) {
#         message(glue::glue("Doing sim {i}"))
#         sim_file <- fread(sims[i])

#         sim_file[, age_band := paste0(floor(age/10) * 10, "-", floor(age/10)*10+9),]
#         sim_file[, day_infection := floor(time_symptoms)]

#         aggregated <- sim_file[, .N, by=list(age_band, day_infection, symptomatic)]
#         aggregated[, PHSM := "medium"]
#         aggregated[, iteration := 1]
#         aggregated[, scenario := str_extract(s, "scenario[0-9]+") ]

#         return (aggregated)
#     })
    
#     return (rbindlist(combined_sims))
# })

# combined_scenarios <- rbindlist(combined_scenarios)

# fwrite(combined_scenarios, "/home/michaell/cm37_scratch/health/NSW_outputs/combined_scenarios_medium.csv")