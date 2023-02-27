library(tidyverse)
library(R.matlab)
library(lubridate)

origin = as_date("2021-02-15")
n_iterations = 500

# Put .mat data files in project directory
file.list = list(
    '/home/michaell/cm37_scratch/health/NSW_outputs/scenario14_2000Omicron_Med_1_full.mat',
    '/home/michaell/cm37_scratch/health/NSW_outputs/scenario25_2000Omicron_Med_1  1  1_full.mat',
    '/home/michaell/cm37_scratch/health/NSW_outputs/scenario26_2000Omicron_Med_1  1  1_full.mat',
    '/home/michaell/cm37_scratch/health/NSW_outputs/scenario2_2000Omicron_Med_1_full.mat',
) %>% setnames({.} %>% str_remove("_.*"))
#file.list = list.files(pattern="\\.mat$") %>%
#  setNames({.} %>% str_remove("_.*"))
#data.list = lapply(file.list, readMat)

process_mat_data = function(mat) {
  mat %>%
    lapply(function(x) {
      if (dim(x)[[1]] > 1) {
        as.vector(t(x))
      } else {
        as.vector(x) %>%
          rep(n_iterations)
      }
    }) %>%
    as_tibble() %>%
    mutate(iteration = rep(seq_len(n_iterations), each=nrow(.)/n_iterations)) %>%
    group_by(iteration) %>%
    mutate(`Cumulative Deaths` = cumsum(daily.deaths.big)) %>%
    ungroup() %>%
    pivot_longer(-day.vec) %>%
    group_by(day.vec, name) %>%
    summarise(mean = mean(value),
              sd = sd(value),
              lower = quantile(value, 0.025),
              median = median(value),
              upper = quantile(value, 0.975),
              .groups = "drop") %>%
    mutate(name = name %>%
             str_remove("(\\.series)?\\.big$") %>%
             fct_recode("Infections (daily)" = "all.infections",
                        "Hospital Admissions (daily)" = "new.admission",
                        "Ward Occupancy" = "ward.OCC",
                        "ICU Occupancy" = "ICU.OCC",
                        "Deaths (daily)" = "daily.deaths") %>%
             fct_relevel(c("Infections (daily)",
                           "Hospital Admissions (daily)",
                           "Ward Occupancy",
                           "ICU Occupancy",
                           "Deaths (daily)",
                           "Cumulative Deaths"))) %>%
    filter(name %>% str_starts("[A-Z]")) # might need more specific rule to remove unused columns
}

plot.data = bind_rows(
  lapply(data.list, process_mat_data),
  .id = "Scenario"
) %>%
  mutate(Scenario = Scenario %>%
           fct_recode("Scenario 26 (??)" = "scenario26"))

ggplot(plot.data, aes(x=day.vec + origin, color=Scenario, fill=Scenario)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha=0.5, color=NA) +
  geom_line(aes(y = median)) +
  geom_vline(xintercept = today(), linetype="dashed", color="grey") +
  facet_wrap(vars(name), ncol=2, scales="free_y") +
  scale_x_date(labels = scales::date_format("%b")) +
  scale_y_continuous(labels = scales::unit_format(unit = "k", scale = 1e-3, sep="")) +
  scale_color_brewer(palette = "Set2") +
  scale_fill_brewer(palette = "Set2") +
  theme_minimal() +
  labs(title = "Title",
       x = NULL,
       y = "Count (median)")