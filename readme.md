# Data Science: Analysis of the customers of a company versus the population at large

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>
Libraries used:  
- matplotlib==3.4.2
- numpy==1.20.2
- pandas==1.4.0
- pandas_stubs==1.2.0.14
- scikit_learn==1.0.2
- xgboost==1.5.2

(The following command can be used to install these: `pip install -r requirements.txt`)

The data files analyzed are provided by Udacity's partners Arvato-Bertelsmann. Permission has not been provided to host them here. If you are attempting to run the jupyter notebooks in this repository, please ensure that the data files are placed in the data folder.

## Project Motivation<a name="motivation"></a>

I want to show that data science can be used to extract insights about the customers (and prospective customers) of a German mail-order sales company, including how the properties of those customers differ from the general German population.

## File Descriptions <a name="files"></a>

`utils.py`  
This module contains the data cleaning functions that are used in the jupyter notebooks.

`Part1_Data_Cleaning.ipynb`  
All the data cleaning steps are fully documented in this notebook. Refactored functions are placed in utils.py and will be reused in Part3.

`Part2_Unsupervised_Machine_Learning.ipynb`   
Unsupervised machine learning (principle component analysis (PCA) and K-means clustering) is used to discover the relationship between the properties of the company's current customers and the properties of the general population.

`Part3_Supervised_Machine_Learning.ipynb`  
Supervised machine learning to try to predict which individuals from a new dataset are likely to become customers. XGBClassifier, AdaBoost, and GradientBoostingClassifer are explored, and AdaBoost is settled on to create the final model.

## Summary of results

The results of this investigation are fully documented both within the notebooks and at the associated medium article.

## Licensing, Authors, and Acknowledgements <a name="licensing"></a>
Author: Dr. Renju Mathew

Thanks to Udacity for the idea for (and structure of) this project. Some of the initial comments provided by Udacity in the originally provided notebook have been altered slightly to make the notebook more readable.  

Thanks to Arvato-Bertelsmann for making their proprietary data available for this project.

