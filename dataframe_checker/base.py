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
            row_view = df.iloc[start_index:end_index].set_index('index')
            print(row_view)

    @classmethod
    def report_missing_value(cls, df: pd.DataFrame, column: str, windows_size: int = 2, show_all: bool = False):
        df = df.copy().reset_index(drop=False)
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
        df = df.copy().reset_index(drop=False)
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
    def report_duplicates_index(cls, df: pd.DataFrame, windows_size: int = 2, show_all: bool = False):
        df = df.copy().reset_index(drop=False)
        duplicate_rows = df[df['index'].duplicated()]
        if duplicate_rows.empty:
            print("No duplicates rows found.")
            return []
        else:
            print("\nRow indices with duplicates index:")
            print(duplicate_rows.index.tolist())

            cls.__showRow(duplicate_rows, df, windows_size, show_all)

            return duplicate_rows.index.tolist()
        


    @classmethod
    def report_skipped_index(cls, df: pd.DataFrame, inferred_freq="D", windows_size: int = 2, show_all: bool = False):
        """
        df: dataframe to check
        inferred_freq: inferred frequency of the index, only apply to datetime index
        windows_size: the size of the window to show
        show_all: if True, show all the skipped indices, otherwise, ask user if continue to show the row view
        """
        df_index = df.index
        sorted_indices = sorted(df_index)
        skipped_indices = []
        nearest_indices = []
        if isinstance(sorted_indices[0], pd.Timestamp):
            min_index = sorted_indices[0]
            max_index = sorted_indices[-1]

            idx_range = pd.date_range(start=min_index, end=max_index, freq=inferred_freq)

            for idx in idx_range:
                if idx not in sorted_indices:
                    skipped_indices.append(idx)
                    nearest_idx = min(sorted_indices, key=lambda x: abs((idx - x).total_seconds()))
                    nearest_indices.append(nearest_idx)


        else:  # Assuming integer indices
            for i in range(sorted_indices[0], sorted_indices[-1]):
                if i not in sorted_indices:
                    skipped_indices.append(i)
                    nearest_idx = min(sorted_indices, key=lambda x: abs(x - i))
                    nearest_indices.append(nearest_idx)

        if not skipped_indices:
            print("No skipped indices found.")
            return []
        else:
            print("\nRow indices with skipped indices:")
            print(skipped_indices)

            df = df.copy().reset_index(drop=False)
            nearest_row = df[df['index'].isin(nearest_indices)]
            cls.__showRow(nearest_row, df, windows_size, show_all)

        return skipped_indices