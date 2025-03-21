import re

import pandas as pd
import numpy as np

from src.ocr.expressions.serachWords.bank_statements import SearchKeywords


#---------------------------------------------------------------------------------------------------------------------------------------
# Cleaning Data
#---------------------------------------------------------------------------------------------------------------------------------------

class CleanData:
    '''
    Class to clean data.
    '''
    @staticmethod
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
    @classmethod
    def check_first_row(cls,df:pd.DataFrame)->bool:
        '''
        Utility function to check if the first row of a dataframe contains more than 3 missing values.

        Args:
            df (pd.DataFrame): The dataframe to check.

        Returns:
            bool: True if the first row contains more than 3 missing values, False otherwise.

        '''
        if df.iloc[0].isna().sum() > 3:
            df.drop(df.index[0], inplace=True)
            return cls.check_first_row(df)
        return True
    @classmethod
    def look_for_header(cls,df:pd.DataFrame):
        '''
        Utility function to check if a dataframe contains a header.

        Args:
            df (pd.DataFrame): The dataframe to check.
            header (list): The header to check for.

        Returns:
            bool: True if the dataframe contains the header, False otherwise.

        '''
        df_copy = df.copy()
        if cls.check_first_row(df_copy):
            if cls.contains_non_english(df_copy.iloc[0][0]):
                df_copy.drop(df_copy.index[0], inplace=True)
            
            #make the first row the header
            df_copy.columns = df_copy.iloc[0]
            df_copy = df_copy.drop(df_copy.index[0])
            df_copy.reset_index(drop=True, inplace=True)
        
        return df_copy


        # Functin to concatinate dfs into ne single dataframe
    @classmethod
    def concat_dfs(cls,dfs: list) -> pd.DataFrame:
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

            df_copy = cls.look_for_header(df_copy)
            
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

    @classmethod
    def clean_df(cls,df:list)->pd.DataFrame:
        '''
        Utility function to clean a dataframe by removing rows with missing values.

        Args:
            df (pd.DataFrame): The dataframe to clean.

        Returns:
            pd.DataFrame: The cleaned dataframe.

        '''
        concatenated_df= cls.concat_dfs(df)

        # concatenated_df.to_csv("final.csv", index=False)
        concatenated_df.dropna(subset=[concatenated_df.columns[0]], inplace=True,how="any")

        return concatenated_df






    #---------------------------------------------------------------------------------------------------------------------------------------
    # Manipulating Data
    #---------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
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
    @classmethod
    def rename_columns(cls,df:pd.DataFrame):
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
            if cls.contains_word(i, SearchKeywords.date_keywords):
                new_columns.append("transaction_date")
            elif cls.contains_word(i, SearchKeywords.description_keywords):
                new_columns.append("transaction_details")
            elif cls.contains_word(i, SearchKeywords.reference_keywords):
                new_columns.append("reference_number")
            elif cls.contains_word(i, SearchKeywords.debit_keywords):
                new_columns.append("debit_amount")
            elif cls.contains_word(i, SearchKeywords.credit_keywords):
                new_columns.append("credit_amount")
            elif cls.contains_word(i, SearchKeywords.balance):
                new_columns.append("balnce")
            
            
            else:
                new_columns.append(i)
        df.columns = new_columns
        
        if 'debit_amount' in df.columns or 'credit_amount' in df.columns:
            df = df.dropna(subset=['debit_amount', 'credit_amount'], how='all')  

            for col in ['debit_amount', 'credit_amount']:  
                if col in df.columns:
                    df.loc[:, col] = df[col].str.replace(',', '').astype(float)

        
        return df
    @classmethod
    async def clean_data(cls, camelot_table) -> pd.DataFrame:
        '''
        Clean and preprocess data extracted from tables using Camelot.

        This function takes a list of Camelot tables and performs data cleaning and preprocessing
        operations to prepare the data for further analysis.

        Args:
            camelot_table (list): A list of Camelot tables extracted from PDF documents.

        Returns:
            pd.DataFrame: A cleaned and preprocessed DataFrame containing the extracted data.

        '''
        df = cls.concat_dfs(camelot_table)  # Call concat_dfs method instead of recursive call
        df = cls.rename_columns(df)
        df.to_csv("final.csv", index=False)
        return df


