import pandas as pd
import numpy as np


def get_extension(file=None):
    """returns file extension"""
    ext = file.split(".")
    if len(ext) > 1:
        return ext[-1]
    return None


def file_extentions():
    """returns dict of file types"""
    return {'blob': ['csv', 'txt', 'json'],
            'matrix': ['xls', 'xlsx']}


def ext_handler(handler):
    """receives an extension argument
    and returns a pandas object handler"""
    ext = {'csv': pd.read_csv,
           'xls': pd.read_excel,
           'xlsx': pd.read_excel,
           'txt': pd.read_csv,
           'json': pd.read_json}
    return ext.get(handler)


def df_replace_value(df, old, new):
    return df.replace(to_replace=old, value=new)


def get_cols(df):
    return list(df.columns)


def format_cols(cols, old=" ", new="_"):
    return [col.lower().replace(old, new) for col in cols]


def df_format_cols(df, cols):
    df.columns = cols
    return df


def convert_timestamps(df, col):
    pd.to_datetime(df[col], errors='coerce').apply(lambda x: x.date())


def num_to_str():
    # TODO: implement
    pass


def str_to_num(df, cols, nulls_as=0, errors='coerce'):
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors=errors)
    df = df.replace(np.nan, nulls_as, regex=True)
    return df


def object_handler():
    # TODO: implement
    pass


def df_set_index(df, index):
    return df.set_index(index)

def null_counts(df, cols):
    return df[cols].isnull().sum(axis=1)