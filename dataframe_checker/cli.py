"""CLI interface for dataframe_checker project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
from base import DataframeChecker
import pandas as pd

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m dataframe_checker` and `$ dataframe_checker `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    data = {
        'A': [0,10000000,2,3,None,5,6,7,8,None,10,11,90000000,13,None,15,16,None,18,19],
    }

    df = pd.DataFrame(data)

    columns_to_check = 'A'
    result = DataframeChecker.report_outliers(df=df, column=columns_to_check, windows_size=2, show_all=False)



if __name__ == "__main__":  # pragma: no cover
    main()