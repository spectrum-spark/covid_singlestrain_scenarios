# Single-strain Modelling of COVID-19: exploration of vaccination and boosting scenarios

This repository contains the source code for an agent-based model of COVID-19 disease spread in a population. In particular, the code produces the model figures and results for a presentation given to IVIRAC on the 13th of February 2023, to form the final report, and for the subsequent scientific publication.

Mathematical modelling assumptions can be found here: [Covid IBM: Waning Immunity](https://spectrum-spark.github.io/covid-IBM/).

### Other relevant models and analysis

The various immunity parameters used were generated using **https://github.com/goldingn/neuts2efficacy**

The cost-effectiveness analysis can be found here: **https://github.com/spectrum-spark/covid-CEA/** 

### Note regarding branches and results

The pink book results come from all the code in the main branch, named [singlestrain-WHO](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO).

The final report with updated plots and additional scenarios come from the branch [singlestrain-WHO-final](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO-final).

Meanwhile, the paper manuscript with arranged output plots come from the branch [singlestrain-paper](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper).


### Code authorship

Major model developement and implementation of the agent-based model was done by Eamon Conway.

The clinical pathways model developement and implementation was done by Camelia Walker.

The vaccine rollout implementation and figures was done by Thao P. Le.

Additional contributes and code checking by Yasmine Mcdonough.

Additional contributions by Logan Wu. 

### Instructions

Immunity parameters were first generated using the [immunity model that extracts vaccine efficacy parameters from antibody titres](https://github.com/goldingn/neuts2efficacy) 

Next, we need to make some initial set up files before the agent-based simuation, in particular, defining the vaccination rollout. This is done in folder [presim_code](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper/presim_code).

The main modelling simulation code is in the folder [main_ABM](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper/main_ABM). The folder contains specific instructions.

The clinical pathways code is in the folder [clinical_pathways](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper/clinical_pathways). The folder contains specific instructions.

The outputs from the clinical pathways is then fed into the [cost-effectiveness analysis](https://github.com/spectrum-spark/covid-CEA/).

Note that there are different pieces of code that require Python, C++, R, and Matlab.

---




*This repository is the code accompaniment to:*


Thao P. Le, Eamon Conway, Edifofon Akpan, Isobel Abell, Patrick Abraham, Christopher M. Baker, Patricia T. Campbell, Deborah Cromer, Michael J. Lydeamore, Yasmine McDonough, Ivo Mueller, Gerard Ryan, Camelia Walker, Yingying Wang, Natalie Carvalho and Jodie McVernon, **Cost-effective boosting allocations in the post-Omicron era of COVID-19 management**, in preparation, 2023.


Eamon Conway, Thao P. Le, Isobel Abell, Patrick Abraham, Edifofon Akpan, Christopher Baker, Mackenzie Bourke, Patricia T. Campbell, Natalie Carvalho, Deborah Cromer, Alexandra B. Hogan, Michael J. Lydeamore, Yasmine McDonough, Ivo Mueller, Gerald Ryan, Camelia Walker, Yingying Wang, and Jodie McVernon, **A flexible immunity model-based framework for evaluation of likely impacts of emerging variants & vaccines: Technical Report**, 2023.

