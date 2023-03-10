# Single-strain Modelling of COVID-19: exploration of vaccination and boosting scenarios

This repository contains the source code for an agent-based model of COVID-19 disease spread in a population. In particular, the code produces the model figures and results for a presentation given to IVIRAC on the 13th of February 2023.

Mathematical modelling assumptions can be found [here: Covid IBM: Waning Immunity](https://spectrum-spark.github.io/covid-IBM/).

The various immunity parameters used were generated using https://github.com/goldingn/neuts2efficacy 

### Code authorship

Major model developement and implementation of the agent-based model was done by Eamon Conway.

The clinical pathways model developement and implementation was done by Camelia Walker.

The vaccine rollout implementation was done by Thao P. Le.

### Instructions

Before the main simulations can be run, some initial set up files need to be created first, in particular, defining the vaccination rollout. This is done in folder [presim_code](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/presim_code).

The main modelling simulation code is in the folder [main_ABM](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/main_ABM). The folder contains specific instructions.

The clinical pathways code is in the folder [clinical_pathways](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/clinical_pathways). The folder contains specific instructions.

Note that there are different pieces of code that require Python, C++, R, and Matlab.

---

*This repository is the code accompaniment to:*

Eamon Conway, Thao P. Le, Isobel Abell, Patrick Abraham, Edifofon Akpan, Christopher Baker, Mackenzie Bourke, Patricia T. Campbell, Natalie Carvalho, Deborah Cromer, Alexandra B. Hogan, Michael J. Lydeamore, Yasmine McDonough, Ivo Mueller, Gerald Ryan, Camelia Walker, Yingying Wang, and Jodie McVernon, **A flexible immunity model-based framework for evaluation of likely impacts of emerging variants & vaccines: Technical Report**, 2023.
