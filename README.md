[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic)](https://github.com/psf/black)
# Reducing Crop Burning to Improve Health and the Environment
## Collaboration across [Energy Harvest Charitable Trust](https://energyharvesttrust.com/), [Carnegie Mellon University](http://www.datasciencepublicpolicy.org/), and [Solve for Good](http://www.solvforgood.org)
### Team

Energy Harvest Charitable Trust: Robery Berry, Priyadeep Kaur, Sukhmeet Singh

CMU and Solve for Good: Sunayana Ghosh (Cervest), Carlos Mougan (University of Southamptom), Rayid Ghani (CMU and Solve for Good)

Google: Niharika Arora

## Overview
This project is aimed at reducing crop burning and air pollution by: 
1. Identifying 
 - when & where farm waste is being burned
 - what and how much is getting burned
2. Intervening: by creating a marketplace for crop residue and connecting farmers, collectors and buyers of crop residue to provide better alternatives and reduce burning
3. Doing Policy advocacy: inform the government about areas where crop waste is getting burned and also, do advocacy for policy changes required for utilization of crop waste

## Report
Current project report is available [here](report.pdf)

## Components
### Detect Fires
#### Data Sources Considered


#### Data Sources Used


#### Analysis and corresponding code


#### List of to-dos

#### References


### Detect Biomass

#### Analysis and corresponding code


#### List of to-dos


#### References



### Identify Crop Type


#### Analysis and corresponding code


#### List of to-dos


#### References


### Detect Amount of Crop

#### Analysis and corresponding code


#### List of to-dos
1. Collect labeled data on fields on the ground. Ideally boxes with lat-long but doesn't need to be too accurate. We'll assume that the parts of an image not labeled as a field is not a field.
2. Identify approaches or models to detect crops/vegetation in satellite images. The goal would be to detect whether asomething is being grown in a given box.
3. Build crop type detectors for each crop that we care about. We've done a first pass on rice but can move to cotton.
4. Estimate size of crop.

#### References



### Other analysis

