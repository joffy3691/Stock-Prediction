
def fit_days_data(df, input_days):

    df1 = df
    df2 = df[-(300 + input_days):]
    df3 = df[-300:]
    return(df1, df2, df3)

