import pandas as pd
from .politeness_v2_helper import *

def get_politeness_v2(df,on_column):
    """ 
    Calculates politness based on Yeomans et. al, 2020: https://www.mikeyeomans.info/papers/receptiveness.pdf, 
    coded into this package: https://github.com/bbevis/SECR 
    
    Args:
        df (pd.DataFrame): The dataframe containing the text on which we wish to apply the feature
        on_column (str): The header of the column containing the text on which this feature will be applied
    
    Returns:
        pd.DataFrame: A dataframe containing the values of linguistic markers that determine politeness
    """

    # Extract column headers by running script on first row
    column_headers = feat_counts(df.iloc[0][on_column],kw)['Features'].tolist()
    
    # Apply the function to each row in text dataframe and store the result in a new output dataframe 
    df_output = df[on_column].apply(lambda x: feat_counts(x,kw)['Counts'])

    # Add column headers
    df_output.columns = column_headers

    return df_output
