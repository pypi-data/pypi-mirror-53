def drop_nulls(df=None, qty=0):
    return df.dropna(thresh=qty)


def drop_all_nulls(df=None):
    return df.dropna(how='all')


def drop_any_nulls(df=None):
    return df.dropna(how='any')


def drop_where_column(df=None, cols=None):
    return df.dropna(subset=cols)
