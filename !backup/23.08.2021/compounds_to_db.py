from bs4 import BeautifulSoup as bs
from build_database import *
from build_database import Compounds
from call_db import *
import requests
import re
import sys
import time


class Comp_to_db:

    def __init__(self, inp_comp, pereodic_table):
        self.inp_comp = inp_comp  # args[0]
        self.pereodic_table = pereodic_table
        self.url = ''
        self.comp_molar_mass = float()
        self.comp_density = float()
        self.comp_nuclides = str()
        self.list_elems = list()
        self.comp_elems = str()
        self.comp_db = Call_comp()

    def __str__(self):
        return f'input:\n formula is {self.inp_comp}, where nuclides are {self.comp_nuclides}'

    def get_nuclides(self):
        self.url = f'https://en.wikipedia.org/wiki/{self.inp_comp}'
        # * drop all numericals from formula and get elements from input
        # * need smth to parse Xn(YnZn)n
        # dr_num = re.findall(r'[A-Z]?[a-z]|[A-Z]', 'NaCl, HCl, H2SO4, Ba(NO3)2, UO2, CaCO3') #* its ok!
        # dr_num = ', '.join(re.findall(r'[A-Z]?[a-z]|[A-Z]', self.inp_comp))
        self.list_elems = re.findall(r'[A-Z]?[a-z]|[A-Z]', self.inp_comp)
        filtr = {k: v[0]
                 for k, v in self.pereodic_table.items() for itm in self.list_elems if itm == k}  # *filter to get name of element
        print(self.list_elems)
        print(filtr.values())
        # print(type(filtr))
        comp = list(filtr.values())  # * names of elements
        self.comp_nuclides = ', '.join(comp)
        return self.scrap_compoud()
        # # self.check_matches(comp) #*? only as concept for now

    def scrap_compoud(self):
        try:
            get = requests.get(self.url)
            print(get)
            soup = bs(get.content, 'html.parser')
            self.comp_name = soup.find(class_='firstHeading').get_text()
            print(self.comp_name)
            get_table = soup.find('table', class_='infobox bordered')
            get_td = get_table.find_all('td')
            query_den_molar = ', '.join(list(i.get_text().strip(
            ) for i in get_td if 'g/mol' in i.get_text() or 'g/cm' in i.get_text() or 'g/L' in i.get_text()))
            print(query_den_molar)
            # mping = map(lambda x: re.findall(r'\d+\.\d+', x), query_txt) #* if query_txt is a list
            mping = re.findall(r'\d+\.\d+', query_den_molar)
            self.molar_mass, self.comp_density = float(
                mping[0]), float(mping[1])
        except Exception as e:
            print(e)
            self.comp_name = input('Type name of compound: ')
            self.molar_mass = float(input('Type molar mass of compound: '))
            self.comp_density = float(input('Type density of compound: '))

        self.comp_elems = ','.join(self.list_elems)
        print(self.comp_elems)
        # data_to_add = Call_comp().table(comp_name=self.comp_name, comp_formula=self.inp_comp,
        #                                 molar_mass=self.molar_mass, density=self.comp_density, nuclides=self.comp_nuclides, nuclides_as_elems=self.comp_elems)
        # Call_comp().add(data=data_to_add)
        # return [self.molar_mass, self.comp_density, self.comp_nuclides, self.comp_elems]

        
        
        
        # def check_matches(self, elems):
        #         print(elems)
        #         if not isinstance(elems, list):
        #             itr = 1
        #         else:
        #             itr = len(elems)
        #         data = Call_mcu().call()
        #         # print(nuclides)
        #         for e in range(itr):
        #             # print(bool((i for i in data if elems[e] in data)))
        #             if not bool((i for i in data if elems[e] in data)):
        #                 raise Exception('No such elem in mcu library')
        #         return


# if __name__ == '__main__':
#     Comp_to_db('Ba(NO3)2').get_nuclides()
#     print(time.process_time())

# 'CaCO3'
# 'NaCl'
# 'HCl'
# 'Ba(NO3)2'


# * template
# * input: formula like: UO2, NACl and so on
# * cols: ['comp_formula', 'comp_name','molar_mass', 'density', 'nuclides']
