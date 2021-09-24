import pandas as pd
import numpy as np
import re
import time
from build_database import *

# df = pd.read_csv('data/mcu_ptr/DEFAULT.PHY', delimiter='\t')
# print(df.head())

class Parsing:
    path = 'data/mcu_ptr/'
    defaultphy = 'DEFAULT.PHY'
    awlib = 'AW.LIB'
    

    def __init__(self):
        self.readlines = tuple()
        self.iso_listDEF = list()
        self.iso_listAW1 = list()
        self.iso_listAW2 = list()
        self.iso_listAW = list()

    # def __str__(self)

    def parsing(self):
        with open(f'{self.path}{self.defaultphy}') as f:
                # print(f.readlines())
            self.readlines = f.readlines()
            # iso_listDEF = (i.split()[0] for i in f if re.findall(r'\w', i.split()[0]))
        self.iso_listDEF = list(i.split()[0] for i in self.readlines if re.findall(r'\w', i.split()[0]))

        with open(f'{self.path}{self.awlib}') as f:
            self.readlines = f.readlines()
            first_part = self.readlines[19:136]
            second_part = self.readlines[145:]
        self.iso_listAW1 = list(i.split() for i in first_part if len(i.split()) >= 3)
        self.iso_listAW2 = list(i.split() for i in second_part if len(i.split()) >= 3)
        self.iso_listAW = self.iso_listAW1 + self.iso_listAW2
        
        def makeSeries(self):
            zipit = list((x,y[1],y[2]) for x in self.iso_listDEF for y in self.iso_listAW if x==y[0])
            print(zipit)
            df = pd.DataFrame(zipit, columns=['Nuclide', 'Code', 'AW'])
            print(df)
            df.to_sql('mcu_iso', engine, index=True, if_exists='replace')
            
        return makeSeries()


if __name__ == '__main__':
    Parsing().parsing()

print(time.process_time())

