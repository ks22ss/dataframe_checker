"""
dataframe_checker base module.

This is the principal module of the dataframe_checker project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
from typing import List
import pandas as pd
# example constant variable
NAME = "dataframe_checker"

class DataframeChecker:

    @classmethod
    def __showRow(cls, results: list, df: pd.DataFrame, windows_size: int, show_all: bool):
        for i, row in results.iterrows():
            if not show_all:
                answer = input("Do you want to continue see the row view? (y/n): ")
                if answer == 'n':
                    print("Stop showing row view.")
                    break
            start_index = max(0, i - windows_size)
            end_index = min(len(df), i + windows_size + 1)
            row_view = df.iloc[start_index:end_index]
            print(row_view)

    @classmethod
    def report_missing_value(cls, df: pd.DataFrame, column: str, windows_size: int = 2, show_all: bool = False):
        df = df.reset_index(drop=False)
        missing_rows = df[df[[column]].isnull().any(axis=1)]
        
        if missing_rows.empty:
            print("No missing values found.")
            return []
        else:
            print("\nRow indices with missing values:")
            print(missing_rows['index'].tolist())

            cls.__showRow(missing_rows, df, windows_size, show_all)

        return missing_rows['index'].tolist()
    
    @classmethod
    def report_outliers(cls, df: pd.DataFrame, column: str, windows_size: int = 2, show_all: bool = False):
        # check if all columns is numeric
        if df.dtypes[column] != 'float64' and df.dtypes[column] != 'int64':
            print("The column is not numeric.")
            return []
        
        # calculate median square error
        df['mse'] = (df[column] - df[column].median() )**2
        threshold = df['mse'].quantile(0.9)

        # find the outliers
        outliers = df[df['mse'] > threshold]
        if outliers.empty:
            print("No outliers found.")
            return []
        else:
            print("\nRow indices with outliers:")
            print(outliers.index.tolist())

            cls.__showRow(outliers, df, windows_size, show_all)

            return outliers.index.tolist()



    @classmethod
    def report_duplicates(cls, df: pd.DataFrame, columns: List[str]):
        pass

    @classmethod
    def report_skipped_index(cls, df: pd.DataFrame, columns: List[str]):
        pass

