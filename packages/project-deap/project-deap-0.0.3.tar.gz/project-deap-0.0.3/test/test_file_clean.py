import pandas as pd, numpy as np
from deap import file_clean as fc

data = {"name": ['Alfred', 'Batman', 'Catwoman'],
        "toy": [np.nan, 'Batmobile', 'Bullwhip'],
        "born": [pd.NaT, pd.Timestamp("1940-04-25"), pd.NaT]}

data_with_null = {"name": [np.nan, 'Batman', 'Catwoman'],
        "toy": [np.nan, 'Batmobile', 'Bullwhip'],
        "born": [np.nan, pd.Timestamp("1940-04-25"), pd.NaT]}


def test_drop_nulls():
    df = pd.DataFrame(data)
    df_size = df.size
    result = fc.drop_nulls(df,3)
    result_size = result.size
    assert result_size < df_size


def test_drop_all_nulls():
    df = pd.DataFrame(data)
    df_size = df.size
    result = fc.drop_all_nulls(df)
    result_size = result.size
    assert result_size == df_size


def test_drop_all_nulls_all_nulls():
    df = pd.DataFrame(data_with_null)
    df_size = df.size
    result = fc.drop_all_nulls(df)
    result_size = result.size
    assert result_size < df_size

def test_drop_any():
    df = pd.DataFrame(data)
    df_size = df.size
    result = fc.drop_any_nulls(df)
    result_size = result.size
    assert result_size < df_size

def test_drop_where_column():
    df = pd.DataFrame(data)
    df_size = df.size
    result = fc.drop_where_column(df, ['born'])
    result_size = result.size
    assert result_size < df_size
