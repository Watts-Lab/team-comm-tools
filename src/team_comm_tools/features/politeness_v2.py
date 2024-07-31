import pandas as pd
from features.politeness_v2_helper import *

def get_politeness_v2(df,on_column):
    """
    @Args:
        The text dataframe
    @Returns:
        The dataframe after adding the politness v2 features
    """

    # Extract column headers by running script on first row
    column_headers = feat_counts(df.iloc[0][on_column],kw)['Features'].tolist()
    
    # Apply the function to each row in text dataframe and store the result in a new output dataframe 
    df_output = df[on_column].apply(lambda x: feat_counts(x,kw)['Counts'])

    # Add column headers
    df_output.columns = column_headers

    return df_output
