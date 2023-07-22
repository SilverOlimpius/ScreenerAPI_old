import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATASHARE = pd.read_csv('DATASHARESfull.csv')

addData = pd.read_csv('AddDATASHARESfull.csv')

merged_df  = pd.concat([DATASHARE, addData])

merged_df.to_csv('merged_df.csv',index=False)

print(merged_df)