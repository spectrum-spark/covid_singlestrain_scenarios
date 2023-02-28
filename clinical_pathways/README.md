# Single-strain Modelling of COVID-19: clinical pathways

### Code authorship

This repository is entirely contributed by Camelia Walker.

### Instructions

The two important functions for us are:

1. **clinical_pathways_immunity_relsev3_func.m**
2. **clinical_knitting_relsev_func.m**

For each output simulation, **clinical_pathways_immunity_relsev3_func** needs to be called to generate the clinical pathway outcomes. Note that each single infection history, the code creates 5 different clinical pathway histories.

Then, when all output simulations (with the same paramters) are done and all singular clinical pathway outcomes are generated, **clinical_knitting_relsev_func** is called to gather all the results into big aggregated files.

An example of how to call these (along with some function parameters) are given in [**example_run.m**](/example_run.m)