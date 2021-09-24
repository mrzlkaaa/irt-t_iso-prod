import pandas as pd
import numpy as np
from build_database import *



# * once used
df = pd.read_html('http://www.science.co.il/elements/', index_col='No.')
print(df)
columns = df[0].columns
query = df[0][['Name','Sym.', 'Atomicweight','Density*(g/cm3)']]
print(query)
query.to_sql('pereodic_table', engine)