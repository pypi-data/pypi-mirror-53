import pandas as pd

def grab(df):
  return(pd.DataFrame(df.isna().sum().sort_values(ascending=False), columns=['NaN Total']))
