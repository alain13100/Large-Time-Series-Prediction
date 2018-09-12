# Author: Youssef Hmamouche

# This file computes reduction methods applicability and the Average Number of the Best Predictors Generated by Each Method

import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

import sys
import os

sys.path.insert(0, 'src/tools')
from csv_helper import *
import os.path

#------------------------------#
#-------- COLORS CLASS --------#
#------------------------------#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#------------------------------#
#------  REDUCED NAMES  -------#
#------------------------------#
def reduce_methods_names (methods):
    reduced_cols = []
    for method in methods:
        if 'Kernel' in method:
            reduced_cols.append ('KPCA')
        elif 'BayeRidge' in method:
            reduced_cols.append ('BayesianRidge')
        elif 'PCA' in method and 'Kernel' not in method:
            reduced_cols.append ('PCA')
        elif 'Hits_te' in method or 'Hits_TE' in method:
            reduced_cols.append ('PEHAR-te')
        elif 'Hits_g' in method:
            reduced_cols.append ('PEHAR-gc')
        elif 'Auto' in method:
            reduced_cols.append ('Arima')
        elif 'Factor' in method:
            reduced_cols.append ('FactA')
        elif 'GFS_te' in method:
            reduced_cols.append ('GFSM-te')
        elif 'GFS_gr' in method:
            reduced_cols.append ('GFSM-gg')
        elif 'Ridge1' in method and 'Ridge' not in reduced_cols:
            reduced_cols.append ('Ridge')
        elif 'Lasso1' in method and 'Lasso' not in reduced_cols:
            reduced_cols.append ('Lasso')
        else:
            reduced_cols.append (method)
    return reduced_cols



# Compute and show evaluation matrix    			   
def main (xls, cols, target_names, reduced_cols, data_name):
    
    measures = ["rmse", "MASE"]
    for measure in measures:
        file = data_name + "_" + measure + "_" + "nb_variables.csv"
        matrix_pf = pd.DataFrame (np.zeros ((len (reduced_cols), len (reduced_cols))))
        df = pd.DataFrame ()
        
        matrix = {}
        for method in cols:
            matrix [method] = [0 for i in range (len (cols))]
        
        number_of_variables = {}
        for method in cols:
            number_of_variables [method] = 0
        
        for target_name in target_names:
            df = pd.DataFrame ()
            for name in sheet_names:
                t_name = name.split('_')[0]
                if target_name != t_name:
                    continue
                df = pd.concat ([df, pd.read_excel(xls, name)], axis = 0)

            if df.empty == True:
                continue

            rmse_values = df[['group',measure]]
            nbre_var = df[['group','method',measure]]
            rmse_values = rmse_values.groupby(['group']).min()
            nbre_var = nbre_var.sort_values(measure).groupby('group', as_index=False).first()
            rmse_values = rmse_values.sort_values(by=[measure])
            nbre_var = nbre_var.sort_values(by=[measure])
            
            INDEX = rmse_values.index
            
            for i in range (len (INDEX)):
                matrix [INDEX[i]][i] = int (matrix [INDEX[i]][i] + 1)

            for i in range(nbre_var.shape[0]):
                nbre_var.iloc[i,1] = str(nbre_var.iloc[i,1]).split (':')[0]

            nb = nbre_var.loc[ nbre_var['group'] == INDEX[0]] [['method']].iloc[0, 0] #.iloc[0,0] #
            number_of_variables [INDEX[0]] = number_of_variables [INDEX[0]] + int (nb)

        for i in range (len (cols)):
            if int (matrix [cols[i]][0]) != 0:
                number_of_variables [cols[i]] = float (number_of_variables [cols[i]]) / float (matrix [cols[i]][0])
            else:
                number_of_variables [cols[i]] = 0

        nbre_var_pf = pd.DataFrame (np.zeros ((len (reduced_cols), 1)))

        # Dict to DaraFrame
        for i in range (len (reduced_cols)):
            for j in range (len (reduced_cols)):
                matrix_pf.iloc [i,j] = matrix [cols[i]][j]

        # Dict to DaraFrame
        for i in range (len (reduced_cols)):
                nbre_var_pf.iloc [i,0] = number_of_variables [cols[i]]

        
	# Store the best number of variables obtained by each method
	nbre_var_pf.index = reduced_cols
        nbre_var_pf.to_csv ("plots/csv/"+ file, sep = ';')
        

	matrix_pf.index = reduced_cols
        #matrix_pf.drop (['Arima'], axis = 0, inplace=True)
        
        '''try:
            matrix_pf.drop (['Ridge'], axis = 0, inplace=True)
        except ValueError:
            print (ValueError)
        
        try:
            matrix_pf.drop (['Lasso'], axis = 0, inplace=True)
        except ValueError:
            print (ValueError)

        try:
            matrix_pf.drop (['BayesianRidge'], axis = 0, inplace=True)
        except ValueError:
            print (ValueError)'''

        matrix_pf.drop (matrix_pf.columns[matrix_pf.shape[0]:], axis = 1, inplace=True)

        INDEX = [i for i in range(1,matrix_pf.shape[0] + 1)]        
        
        plt.gcf().subplots_adjust(left=0.20, bottom=0.10)
        sns.heatmap(matrix_pf, xticklabels = INDEX, annot=True,linewidths=.5, annot_kws={'size':8}, cmap="Blues", robust=True, fmt = 'g')
        plt.setp (plt.gca().yaxis.get_majorticklabels(), rotation='horizontal')

        if "ausmacro" in data_name:
            data_name = "aus"
        plt.savefig ("plots/pdf/" + data_name + "_" + measure + ".pdf")        
        #plt.show()
        plt.clf ()


#    MAIN     
if __name__ == "__main__":
    
    if len (sys.argv) < 2:
        print ( bcolors.FAIL + "Unsufficient arguments! add the data path." + bcolors.ENDC)
        exit (1)
    
    #------ READ DATA ---------#
    file_name = sys.argv[1]
    data_name = file_name.split('/')[-1].split('.')[0]


    #------ READ TARGET NAMES ---------#
    target_names = read_csv_and_metadata (file_name).meta_header['predict']
    #exit (1)

    #------ READ SHEET NAMES ---------#
    if os.path.exists ("results/evaluation/" + data_name + "/" + data_name + ".xlsx"):
        xls = pd.ExcelFile("results/evaluation/" + data_name + "/" + data_name + ".xlsx")
    elif os.path.exists ("results/evaluation/" + data_name + "/" + data_name + ".xls"):
        xls = pd.ExcelFile("results/evaluation/" + data_name + "/" + data_name + ".xls")
    else:
        print ("Error in reading the file: " + data_name)
        #exit (1)
    
    sheet_names = xls.sheet_names
    df = pd.read_excel(xls, sheet_names[0])
    cols, counts = np.unique(df['group'], return_counts=True)

    for i in range(len (sheet_names)):
        df = pd.read_excel(xls, sheet_names[i])
        cols_ = np.unique(df['group'])
        cols = np.concatenate ((cols, cols_), axis = 0)

    cols = np.unique(cols)

    #------ CONSTRUCT REDUCED NAMES ---------#
    reduced_cols = reduce_methods_names (cols)
    
    #------------- MAIN ---------------#
    main (xls, cols, target_names, reduced_cols, data_name)


























