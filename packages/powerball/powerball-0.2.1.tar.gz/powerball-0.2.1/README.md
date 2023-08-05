<center><h1>Powerball
 <h3>A Tool for Competitive Lottery Analysis of Bacterial Groups </h3>
 by Matthew Marshall and John Darcy</center>
 
 ---
 
### What is Competitive Lottery Analysis?

Competitive Lottery Analysis is examining the competitiveness and "lottery-ness" of a number of groups in a specific kind of environment. A competitive lottery environment is one where many species are competing for dominance of a small number of sites or patches. Species in these environments will either dominate a site, forcing all other species out, or will coexist with other species on that patch. Here we define competitiveness as the degree to which a group is consistently dominated by a small number of species within that group, and lottery-ness, which we define as the extent to which the same species will always dominate within a particular group of species. Competitive lottery analysis allows us to explore those metrics by analyzing population data to see which groups of species, are competitive, how competitive they are relative to other species, and how deterministically they dominate their groups.

### What is Powerball?

Powerball is a Python 3 command-line tool that can be used to perform competitive lottery analysis of user-defined groups of species using Monte Carlo Simulation. It was developed for a research project as part of the Colorado Biomedical Informatics Summer Training Fellowship at the University of Colorado Anschutz Medical Campus. The use-cases for PowerBall are varied, and clinically relevant. For example, users can find which bacteria are competing with potential pathogens, and the extent to which that competition regularly occurs. Both the competitiveness and lottery-ness results of this analysis could inform patient outcome predictions as well as potential treatment plans. This knowledge provides valuable medical insight and may help inform the discovery of novel or probiotic treatments and inform treatment decisions for known pathogens. Additionally, PowerBall can be used in an ecological research framework using many different samples to better examine how competitiveness and/or lottery-ness change across environments, across patients, or across time.

### Installation

You can install Powerball through the Python Package Index (PyPI) by running `pip install powerball`

### Usage

Powerball takes one mandatory argument: the name of an input csv file where each row represents a species and each column represents a sample of population data about that species. The final column of the table is a string used for grouping species based on some user-defined grouping parameter. For example, you could decide that all species that are taxonomically similar belong in the same group. An example of what an input file should look like is given by the table below and in data/example.csv:


|Species      |Sample A |Sample B |Sample C |Sample D |Sample E| Groups |
|---          | ---     | ---     | ---     | ---     | ---    | ---    |
|**Species 1**| 30      | 10      | 30      | 10      | 10     | Group 1|
|**Species 2**| 15      | 20      | 25      | 11      | 15     | Group 1|
|**Species 3**| 20      | 5       | 15      | 18      | 0      | Group 1|
|**Species 4**| 5       | 0       | 10      | 13      | 5      | Group 2|
|**Species 5**| 10      | 5       | 0       | 14      | 20     | Group 2|
|**Species 6**| 15      | 30      | 0       | 10      | 20     | Group 2|
|**Species 7**| 10      | 10      | 20      | 5       | 34     | Group 3|
|**Species 8**| 5       | 10      | 17      | 0       | 0      | Group 3|
|**Species 9**| 5       | 17      | 3       | 25      | 20     | Group 3|

Powerball has a minimum group size of 3 (each group must have at least 3 rows). Any groups below that minimum will be ignored. A warning will be displayed if any groups are ignored, and the names of the groups will be shown. This minimum group size can be changed through the command line argument `-gs` or `--groupSize` by specifying a number after it.

<br/>

Basic usage for Powerball is `python powerball.py filename.csv` This is run from the root directory of the project and filename.csv can be renamed to anything as long as it ends in .csv

This will show the competitiveness score, lottery score, and p-values for all groups, all rounded to 4 decimal places. See the image below for an example:


![](images/basicRun.png)

This data is also saved to an output csv file (default name is Output.csv)

<br/>
For more advanced usage, Powerball has many different command line arguments. A full list can be shown by running `python powerball.py --help` or `python powerball.py -h`


![](images/args.png)

Powerball automatically generates an interactive graph of the output data using Bokeh (this can be silenced using the --chartStyle argument with a value greater than 3)

## How Does it Work?

The input data specified in the csv file is used to generate a list of **Shannon Diversity** scores for each group. Shannon Diversity 	diversity is a statistical measure of the diversity of a community given by the formula:

![](images/shannonFormula.svg)

where p<sub>i</sub> is the proportion of individuals belonging to the ith species in the group and R is the richness or number of species within a group.

The diversity scores for a group are then compared against a null distribution of scores generated through **Permutational Monte Carlo simulation**.

The scores within the null distribution are diversity scores for a random group of the same size created by permuting all rows (including species not within the group of interest) of the input matrix.

This process is repeated until a sufficiently large distribution is generated for each group (number of simulations is controlled by the `--nullSize` argument, with a default value of 1000)

Observing diversity scores which are higher than expected by the null hypothesis would imply relatively even population distribution between the species of a group. This would also imply that more competition exists within that group. We define competitiveness as the **Standardized Effect Size** of the group, given by the formula:



![](images/standardEffectFormula.svg)

where μ<sub>1</sub> is the mean for our empirical Shannon Diversity data, μ<sub>2</sub> is the mean for the null distribution, and σ is the standard deviation based on the null distribution. 


**Lottery scores**, which represent how deterministically a species dominates its group, are also generated through Permutational Monte Carlo simulation, with two key differences:

1. Instead of generating diversity scores by permuting the rows of the input matrix, we permute the columns within each group. 

2. Diversity scores are taken from row sums instead of the entire row.

Competitiveness scores and lottery scores both have **1-tailed P-values**, calculated permutationally as the proportion of values in the null distribution more extreme than the observed value.