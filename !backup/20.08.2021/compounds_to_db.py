from bs4 import BeautifulSoup as bs
from build_database import *
from build_database import Compounds
from call_db import *
import requests
import re
import sys
import time


class Comp_to_db:

    def __init__(self, inp_comp):
        self.inp_comp = inp_comp  # args[0]
        self.url = ''
        self.comp_molar_mass = float()
        self.comp_density = float()
        self.comp_nuclides = str()
        self.comp_db = Call_comp()

    def __str__(self):
        return f'input:\n formula is {self.inp_comp}, where nuclides are {self.comp_nuclides}'

    def get_nuclides(self):

        to_dict = {i[2]: [i[1], i[3], i[4]] for i in Call_PT().call()}
        if len(self.inp_comp) < 3:
            elem, self.molar_mass, self.comp_density = to_dict[self.inp_comp][
                0], to_dict[self.inp_comp][1], to_dict[self.inp_comp][2]
            # self.check_matches(elem)  #*? only as concept for now (# * run func to ckeck mathes with mcu lib)
            self.url = f'https://en.wikipedia.org/wiki/{elem}'
            print(self.molar_mass, self.comp_density)
            return
        else:
            print(self.comp_db.check_exists(self.inp_comp))
            if not self.comp_db.check_exists(self.inp_comp):
                # * drop all numericals from formula and get elements from input
                # * need smth to parse Xn(YnZn)n 
                # dr_num = re.findall(r'[A-Z]?[a-z]|[A-Z]', 'NaCl, HCl, H2SO4, Ba(NO3)2, UO2, CaCO3') #* its ok!
                # dr_num = ', '.join(re.findall(r'[A-Z]?[a-z]|[A-Z]', self.inp_comp))
                get_elems = re.findall(r'[A-Z]?[a-z]|[A-Z]', self.inp_comp)
                filtr = {k: v[0]
                         for k, v in to_dict.items() for itm in get_elems if itm == k}  # *filter to get name of element
                self.url = f'https://en.wikipedia.org/wiki/{self.inp_comp}'
                print(get_elems)
                print(filtr.values())
                # print(type(filtr))
                comp = list(filtr.values())  # * names of elements
                self.comp_nuclides = ', '.join(comp)
                return self.scrap_compoud()
            else:
                print(self.comp_db.call_existing(self.inp_comp))
                self.molar_mass, self.comp_density, self.comp_nuclides = self.comp_db.call_existing(
                    self.inp_comp)
            # self.check_matches(comp) #*? only as concept for now

    def check_matches(self, elems):
        print(elems)
        if not isinstance(elems, list):
            itr = 1
        else:
            itr = len(elems)
        data = Call_mcu().call()
        # print(nuclides)
        for e in range(itr):
            # print(bool((i for i in data if elems[e] in data)))
            if not bool((i for i in data if elems[e] in data)):
                raise Exception('No such elem in mcu library')
        return

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
            self.molar_mass = float(input('Type density of compound: '))

        data_to_add = Call_comp().table(comp_name=self.comp_name, comp_formula=self.inp_comp,
                                        molar_mass=self.molar_mass, density=self.comp_density, nuclides=self.comp_nuclides)
        return Call_comp().add(data=data_to_add)


if __name__ == '__main__':
    Comp_to_db('Ba(NO3)2').get_nuclides()
    print(time.process_time())

# 'CaCO3'
# 'NaCl'
# 'HCl'
# 'Ba(NO3)2'


# * template
# * input: formula like: UO2, NACl and so on
# * cols: ['comp_formula', 'comp_name','molar_mass', 'density', 'nuclides']
