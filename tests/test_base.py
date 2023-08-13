from dataframe_checker.base import DataframeChecker
import pandas as pd

def test_report_missing_value():
    data = {
        'A': [0, 1, 2, 3, 4,5,6,7,8,9,10,None,12,13,14,15,16,17,18,19],
        'B': [None, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        'C': [0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,None]
    }

    index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    df = pd.DataFrame(data, index=index)

    columns_to_check = 'A'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [11]

    columns_to_check = 'B'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [0]

    columns_to_check = 'C'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [19]

    index = pd.date_range('1/1/2000', periods=20)
    df = pd.DataFrame(data, index=index)

    columns_to_check = 'A'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [pd.Timestamp('2000-01-12 00:00:00')]

    columns_to_check = 'B'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [pd.Timestamp('2000-01-01 00:00:00')]

    columns_to_check = 'C'
    result = DataframeChecker.report_missing_value(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [pd.Timestamp('2000-01-20 00:00:00')]


def test_report_outliers():
    data = {
        'A': [0,1,2,3,4,5,6,7,8,9000000],
        'B': [0,1,2,3,4,5,6000000,7,8,9],
        'C': [0,1000000,2,3,4,5,6,7,8,9]
    }

    index = [0,1,2,3,4,5,6,7,8,9]
    df = pd.DataFrame(data, index=index)

    columns_to_check = 'A'
    result = DataframeChecker.report_outliers(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [9]

    columns_to_check = 'B'
    result = DataframeChecker.report_outliers(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [6]

    columns_to_check = 'C'
    result = DataframeChecker.report_outliers(df=df, column=columns_to_check, windows_size=2, show_all=True)
    assert result == [1]
