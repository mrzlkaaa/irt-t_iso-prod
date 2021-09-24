import pandas as pd
import numpy as np
from build_database import *



# * once used
# df = pd.read_html('http://www.science.co.il/elements/', index_col='No.') #*GOT FROM URL
df = pd.read_sql('pereodic_table', engine,index_col='index') # index_col='No.')
df['Nuclear_Density'] = 0.602*df['Density*(g/cm3)'].astype(float)/df['Atomicweight'].astype(float)
# df[0][['Atomicweight','Density*(g/cm3)']].astype(float)
print(df)
# columns = df[0].columns
# query = df[['Name','Sym.', 'Atomicweight','Density*(g/cm3)']]
# # # print(query)
df.to_sql('pereodic_table', engine, if_exists='replace')