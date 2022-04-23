#!/bin/sh
for (( i=1; i<=50; i++ ))
do
  ./RunInitialandWinterWave state_parameters/omicron_update_VE_updated.json winter_wave_scenarios/sim_params_v1.json $i  winter_wave_scenarios initial-and-during_vax_infect_scenario1_older
done
