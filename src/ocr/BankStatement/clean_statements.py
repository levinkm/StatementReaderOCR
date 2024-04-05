import re

import pandas as pd
import numpy as np


#---------------------------------------------------------------------------------------------------------------------------------------
# Cleaning Data
#---------------------------------------------------------------------------------------------------------------------------------------


def contains_non_english(word) -> bool:
    '''
    Utility function to check if a word contains non-English characters.

    Args:
        word (str): The word to check.

    Returns:
        bool: True if the word contains non-English characters, False otherwise.

    '''
    if not isinstance(word, str):
        return True
    non_english_pattern = re.compile(r'[^\x00-\x7F]+')
    return bool(non_english_pattern.search(word)) 


# functin to check if the first row has more than 3 missing values hence deleting it until it get's one with less than 3 nissing values
def check_first_row(df:pd.DataFrame)->bool:
    '''
    Utility function to check if the first row of a dataframe contains more than 3 missing values.

    Args:
        df (pd.DataFrame): The dataframe to check.

    Returns:
        bool: True if the first row contains more than 3 missing values, False otherwise.

    '''
    if df.iloc[0].isna().sum() > 3:
        df.drop(df.index[0], inplace=True)
        return check_first_row(df)
    return True

def look_for_header(df:pd.DataFrame):
    '''
    Utility function to check if a dataframe contains a header.

    Args:
        df (pd.DataFrame): The dataframe to check.
        header (list): The header to check for.

    Returns:
        bool: True if the dataframe contains the header, False otherwise.

    '''
    df_copy = df.copy()
    if check_first_row(df_copy):
        if contains_non_english(df_copy.iloc[0][0]):
            df_copy.drop(df_copy.index[0], inplace=True)
        
        #make the first row the header
        df_copy.columns = df_copy.iloc[0]
        df_copy = df_copy.drop(df_copy.index[0])
        df_copy.reset_index(drop=True, inplace=True)
    
    return df_copy


    # Functin to concatinate dfs into ne single dataframe
def concat_dfs(dfs: list) -> pd.DataFrame:
    """
    Concatenate multiple dataframes into a single dataframe.

    Args:
        dfs (list): A list of dataframes to concatenate.

    Returns:
        pd.DataFrame: The concatenated dataframe.
    """
    fin = pd.DataFrame()  # Initialize an empty DataFrame
    for index,df in enumerate(dfs):
        # Make a copy to avoid unintended modifications
        df_copy = df.df.copy()   # Create a copy

        # Reset the index of the DataFrame copy
        df_copy.reset_index(drop=True, inplace=True)

        df_copy.replace('',np.nan,inplace=True)

        df_copy = look_for_header(df_copy)
        
        # Concatenate only if columns match
        if fin.shape[1] != df_copy.shape[1]:
            if fin.shape[1] == 0:
                fin = df_copy.copy()
            elif df_copy.shape[1] == 0:
                continue
            elif fin.shape[1] > df_copy.shape[1]:

                pass
            else:
                
                fin = pd.DataFrame()  # Reset fin DataFrame
                fin = pd.concat([fin.reset_index(drop=True), df_copy.reset_index(drop=True)], ignore_index=True)
                
        else:
            
            fin = pd.concat([fin.reset_index(drop=True), df_copy.reset_index(drop=True)], ignore_index=True)
            
            

    return fin


def clean_df(df:pd.DataFrame)->pd.DataFrame:
    '''
    Utility function to clean a dataframe by removing rows with missing values.

    Args:
        df (pd.DataFrame): The dataframe to clean.

    Returns:
        pd.DataFrame: The cleaned dataframe.

    '''
    concatenated_df=concat_dfs(df1)# type: ignore

    # concatenated_df.to_csv("final.csv", index=False)
    concatenated_df.dropna(subset=[concatenated_df.columns[0]], inplace=True,how="any")

    return concatenated_df



from Expressions.serachWords.bank_statements import SearchKeywords


#---------------------------------------------------------------------------------------------------------------------------------------
# Manipulating Data
#---------------------------------------------------------------------------------------------------------------------------------------

def contains_word(text: str, word_list: list[str]) -> bool:
    """
    Utility function to check if a text contains a word from a given list.

    Args:
        text (str): The text to check.
        word_list (list): The list of words to check for.

    Returns:
        bool: True if the text contains a word from the list, False otherwise.
    """
    for word in word_list:
        if str(word).lower() in str(text).lower():
            return True
    return False

# function to rename the columns based on the current column namess by using a wordlis 
def rename_columns(df:pd.DataFrame):
    """
    Rename columns of a DataFrame based on the given word list.

    Args:
        df (pd.DataFrame): The DataFrame whose columns are to be renamed.
        wordlist (list): List of keywords to identify column names.

    Returns:
        pd.DataFrame: DataFrame with renamed columns.
    """
    new_columns = []
    for i in df.columns:
        if contains_word(i, SearchKeywords.date_keywords):
            new_columns.append("transaction_date")
        elif contains_word(i, SearchKeywords.description_keywords):
            new_columns.append("transaction_details")
        elif contains_word(i, SearchKeywords.reference_keywords):
            new_columns.append("reference_number")
        elif contains_word(i, SearchKeywords.debit_keywords):
            new_columns.append("debit_amount")
        elif contains_word(i, SearchKeywords.credit_keywords):
            new_columns.append("credit_amount")
        elif contains_word(i, SearchKeywords.balance):
            new_columns.append("balnce")
        
        
        else:
            new_columns.append(i)
    df.columns = new_columns
    if 'debit_amount' in df.columns:
        df = df.dropna(subset=['debit_amount'])
        df.loc[:,'debit_amount'] = df['debit_amount'].str.replace(',', '').astype(float)
    
    if 'credit_amount' in df.columns:
        df = df.dropna(subset=['credit_amount'])
        df.loc[:,'credit_amount'] = df['credit_amount'].str.replace(',', '').astype(float)

    
    return df

def clean_data(camelot_table: list) -> pd.DataFrame:
    '''
    Clean and preprocess data extracted from tables using Camelot.

    This function takes a list of Camelot tables and performs data cleaning and preprocessing
    operations to prepare the data for further analysis.

    Args:
        camelot_table (list): A list of Camelot tables extracted from PDF documents.

    Returns:
        pd.DataFrame: A cleaned and preprocessed DataFrame containing the extracted data.

    '''
    df = concat_dfs(camelot_table)
    df = rename_columns(df)
    return df


