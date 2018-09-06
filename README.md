# Thesis Experiments

This file contains the used data, the models and methods implementations,  and the results associated with the work of the thesis. The results include the default graphs, the results of the variable selection and prediction stage, and finally the prediction evaluations.

# Structure:

## data: the used multivariate time series

## src: methdods and models implementations

	* tools: some function for reading and writing files and metadata

	* pre_selection: causality graphs computation with the granger causality and the transfert entropy

	* selection: feature selection methods

	* prediction: the implementations of the prediction models
	
	* pre_evaluation: scripts for gathering the prediction errors
	
	* evaluation: compute the forecast accuracy using MASE and RMSE measures.
	
		
## results

	* pre_selection: causality matrix of each datasets

	* selection: feature selection (with all methods) for each target variable of each datasets.

	* prediction: the prediction associated to each file from src/selection/

      
# Installation

  * install dependencies for python
    ```bash
    pip install -r requirements.txt.
    ```
   * install dependencies for R
   Rscrip requirements.R
