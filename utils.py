print("utils loaded: this module contains helpful data cleaning functions")
import numpy as np
import pandas as pd

# I have manually identified the categorical variables from the relevant Excel file :
categorical_variables =  ['AGER_TYP',  'ANREDE_KZ', 'BIP_FLAG', 'CAMEO_DEUG_2015', 'CAMEO_DEU_2015',
'CJT_GESAMTTYP', 'D19_KONSUMTYP', 'FINANZTYP', 'GEBAEUDETYP','GFK_URLAUBERTYP', 'GREEN_AVANTGARDE', 
'HAUSHALTSSTRUKTUR', 'KBA05_MAXHERST', 'LP_FAMILIE_FEIN', 'NATIONALITAET_KZ', 'OST_WEST_KZ',  'SHOPPER_TYP', 
'SOHO_FLAG', 'TITEL_KZ', 'VERS_TYP', 'ZABEOTYP']

#### For later reference, I have listed here the meanings of the above.
# AGER_TYP	best-ager typology
# ANREDE_KZ	gender
# BIP_FLAG	business-flag indicating companies in the building
# CAMEO_DEUG_2015	CAMEO classification 2015 - Uppergroup
# CAMEO_DEU_2015	CAMEO classification 2015 - detailed classification
# CJT_GESAMTTYP	customer journey typology
# D19_KONSUMTYP	consumption type 
# FINANZTYP	best descirbing financial type for the person
# GEBAEUDETYP	type of building (residential or commercial)
# GFK_URLAUBERTYP	vacation habits
# GREEN_AVANTGARDE	the environmental sustainability is the dominating movement in the youth of these consumers
# HAUSHALTSSTRUKTUR	structure of the household (single-hh, couple with different surnames, family,...)
# KBA05_MAXHERST	most common car manufacturer in the microcell
# LP_FAMILIE_FEIN	family type fine
# NATIONALITAET_KZ	nationaltity (scored by prename analysis)
# OST_WEST_KZ	flag indicating the former GDR/FRG
# SHOPPER_TYP	shopping typology
# SOHO_FLAG	small office/home office flag
# TITEL_KZ	flag whether this person holds an academic title
# VERS_TYP	insurance typology 
# ZABEOTYP	typification of energy consumers

### Notes:

# I think KBA05_MODTEMP may have been a categorical variable, but the documentation was unclear to me.

# CAMEO_DEUINTL_2015	CAMEO classification 2015 - international typology -- 
# No additional information is gained by using this as this is effectively same as CAMEO_DEU_2015
# except that it is coded differently.

# 'LP_STATUS_GROB' is also not used as it contains the same info as LP_FAMILIE_FEIN


def drop_columns_and_rows(df, columns_to_drop, missing_values_threshold_row=np.inf):
    '''
    Drops columns from df that are in columns_to_drop.
    Drops rows where the number of missing values is above missing_values_threshold_row
    If no missing_values_threshold_row is supplied, no rows are removed.
    '''
    df_clean = df.copy()
    
    # Drop appropriate columns
    df_clean = df_clean.drop(columns_to_drop, axis = 1)
    
    # Keep rows that have missing values less than missing_values_threshold_row
    df_clean = df_clean[ df_clean.isnull().sum(axis =1) < missing_values_threshold_row ]
    
    return df_clean

def drop_columns_and_rows_percent(df, missing_columns_percent=20.0, missing_rows_percent = 10.):
    '''
    TODO
    '''
    null_df_percent= 100 * df.isnull().sum(axis=0) / (df.shape[0])
    columns_missing_x_percent = null_df_percent[null_df_percent>missing_columns_percent].index.tolist()
    print("{} columns are missing {} of their values".format(len(columns_missing_x_percent), missing_columns_percent))
    df_clean = df.copy()
    
    # Drop appropriate columns
    print("Dropping these columns: {}".format(columns_missing_x_percent))
    df_clean = df_clean.drop(columns_missing_x_percent, axis = 1)
    
    # Keep rows that have missing values less than missing_values_threshold_row
    null_df_percent= 100 * df.isnull().sum(axis=1) / (df.shape[1])
    null_df_percent.sort_values(ascending = False, inplace = True)
    missing_rows_percent = 10.0
    missing_values_threshold = np.floor(df.shape[1]*missing_rows_percent*0.01)
    cut_off = sum(null_df_percent < missing_rows_percent) / len(null_df_percent)
    print("Drop rows containing more than {}% of their values (i.e. {} missing values.)".format(missing_rows_percent, missing_values_threshold))
    print("{}% of the rows are missing {}% of their values".format(round(100*(1-cut_off)), missing_rows_percent))
    
    df_clean = df_clean[ df_clean.isnull().sum(axis =1) < missing_values_threshold ]
    
    return df_clean

def handle_categorical(df_original, categories_to_handle):
    '''
    Check which columns from categories_to_handle contain non binary non-numerical values

    Convert these categorical variables into dummy/indicator variables. 
    New columns are created. (Original categorical variables are dropped)
    
    
    This function also drops from df_original the following undocumented columns:
    'EINGEFUEGT_AM', 'CAMEO_INTL_2015'
    This function drops D19_LETZTER_KAUF_BRANCHE because it contains too many unique values
    '''
    
    df = df_original.copy()
    binary_numerical_features = []
    binary_non_numerical_features = []
    non_binary_features = []
    for category in categories_to_handle:
        distinct_values = (df[category].unique())
        if len(distinct_values) == 2 and distinct_values.dtype != 'object':
            #print('BINARY NUMERICAL')
            #print (distinct_values)
            binary_numerical_features.append(category)
        elif len(distinct_values) == 2 and distinct_values.dtype == 'object':
            #print('BINARY NON-NUMERICAL')
            #print (distinct_values)
            binary_non_numerical_features.append(category)
        else:
            #print('NONBINARY')
            #print (distinct_values)
            non_binary_features.append(category)
            
    df['OST_WEST_KZ'] = df['OST_WEST_KZ'].replace("O", "0")
    df['OST_WEST_KZ'] = df['OST_WEST_KZ'].replace("W", "1")
    df['OST_WEST_KZ'] = df['OST_WEST_KZ'].astype(float)
    
    # We'll drop these as they are undocumented. (Assuming they haven't been dropped already)
    try:
        df.drop('EINGEFUEGT_AM', axis=1, inplace=True)
        df.drop('CAMEO_INTL_2015', axis=1, inplace=True)
        df.drop('D19_LETZTER_KAUF_BRANCHE', axis=1, inplace=True) # Too many values
    except:
        pass
    
    df_new =  df.copy()
    for attribute in non_binary_features:
        dummy_columns = pd.get_dummies(df_original[attribute], prefix = attribute)
        df_new = df_new.join(dummy_columns)
        
    # Now that the categories have been encoded numerically,
    # drop the original categories
    df_new = df_new.drop(non_binary_features, axis = 1)
    print("Original columns are dropped")
    return df_new

def print_list(a_list, sep = ", "):
    ''' Prints a list in a space saving way'''
    a_list = list(a_list)
    num_items = len(a_list)
    for i in range(num_items):
        if i == num_items-1:
            print(a_list[i], end = "")
        else:
            print(a_list[i], end = sep)
            
def replace_symbols_with_nan(df, columns, symbols):
    '''For each column in the dataframe, values in the `symbols` list are replaced with nan'''
    df_clean = df.copy()
    for column in columns:
        try:
            df_clean[column] = df_clean[column].replace(symbols, value=np.nan)
        except:
            print("No appropriate value found in ", column)
    return df_clean

def unknown_to_nan(df, dict_of_unknowns):
    '''
    INPUT:
    df - pandas dataframe 
    dict_of_unknowns - key-value pairs, where values indicate "unknown" 
    
    OUTPUT:
    df - dataframe
    
    Description:
    Checks values df against dict_of_unknowns
    Return a dataframe with unknown values replaced with nan.
    '''
    df_new = df.copy() # Don't change the original dataframe
    for attribute, value in dict_of_unknowns.items():
        if attribute in df.columns:
            for i in range(len(value)):
                #print(key, value[i])
                df_new.loc[ df_new[attribute] == int(value[i]) , attribute ] = np.nan
    return df_new