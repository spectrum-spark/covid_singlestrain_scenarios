library(data.table)

df_baseline <- fread("/home/michaell/cm37_scratch/health/NSW_outputs/combined_scenarios_baseline_par.csv")

#Scenario
rolling_mean <- df_baseline[scenario == "scenario26", .(N=frollsum(N, n=7), day_infection), by=list(iteration)]

max_day <- rolling_mean[, median(N, na.rm=T), by=day_infection][which.max(V1), day_infection]

rolling_baseline <- df_baseline[order(day_infection)][scenario == "scenario26", .(N, rolling_N=frollsum(N, n=7), day_infection), by=list(age_band,iteration,symptomatic)]

rolling_baseline_median <- rolling_baseline[, .(N=median(N), rolling_N=median(rolling_N, na.rm=T)), by=list(age_band, symptomatic, day_infection)]
baseline_table <- rolling_baseline[day_infection == max_day, .(N=sum(median(rolling_N, na.rm=T))), by=list(age_band, symptomatic)][, booster_timing := "5months"]

fwrite(baseline_table, "~/baseline_peak_5month.csv")
fwrite(rolling_baseline_median, "~/baseline_rolling_timeseries_5month.csv")
fwrite(rolling_baseline_median[, .(N=sum(N), rolling_N=sum(rolling_N)), by=list(day_infection, symptomatic)], "~/baseline_rolling_timeseries_aggregated_5month.csv")


df_low <- fread("/home/michaell/cm37_scratch/health/NSW_outputs/combined_scenarios_low_par.csv")

#Scenario
rolling_mean <- df_low[scenario == "scenario25", .(N=frollsum(N, n=7), day_infection), by=list(iteration)]

max_day <- rolling_mean[, median(N, na.rm=T), by=day_infection][which.max(V1), day_infection]

rolling_low <- df_low[order(day_infection)][scenario == "scenario26", .(N, rolling_N=frollsum(N, n=7), day_infection), by=list(age_band,iteration,symptomatic)]
rolling_low_median <- rolling_low[, .(N=median(N), rolling_N=median(rolling_N, na.rm=T)), by=list(age_band, symptomatic, day_infection)]
low_table <- rolling_low[day_infection == max_day, .(N=sum(median(rolling_N, na.rm=T))), by=list(age_band, symptomatic)][, booster_timing := "4months"]
fwrite(low_table, "~/low_peak_4month.csv")
fwrite(rolling_low_median, "~/low_rolling_timeseries_4month.csv")
fwrite(rolling_low_median[, .(N=sum(N), rolling_N=sum(rolling_N)), by=list(day_infection, symptomatic)], "~/low_rolling_timeseries_aggregated_4month.csv")
