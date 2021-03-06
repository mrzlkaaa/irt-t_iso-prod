from bs4 import BeautifulSoup as bs
from build_database import *
from build_database import Compounds
import asyncio
from call_db import *
import requests
import re
import sys
import time
import copy


class Comp_to_db:

    def __init__(self, inp_comp, pereodic_table):
        self.inp_comp = inp_comp
        self.pereodic_table = pereodic_table
        self.url = f'https://en.wikipedia.org/wiki/{self.inp_comp}'
        self.comp_db = Call_comp()
        self.coeffs = {}
        self.nuc_dens = {}
        self.NA = 0.602

    def __str__(self):
        return f'input:\n formula is {self.inp_comp}, where nuclides are {self.comp_nuclides}'

    async def get_nuclides(self):
        print('get_nucl has started')
        self.list_elems = re.findall(r'[A-Z][a-z]?', self.inp_comp)
        print(self.list_elems)
        self.comp_elems = ','.join(self.list_elems)
        filtr = {k: v[0]
                 for k, v in self.pereodic_table.items() for itm in self.list_elems if itm == k}  # *filter to get name of element
        print(filtr)
        await asyncio.sleep(0.25)
        self.comp_nuclides = ', '.join(list(filtr.values())) #* names of elements
        print('get_nucl has finished')
        get_coeffs = asyncio.create_task(self.get_coeffs())
        await get_coeffs
        return 

    async def scrap_compoud(self):
        print('scrap has started')
        get = requests.get(self.url)
        print(get.elapsed.total_seconds())
        await asyncio.sleep(get.elapsed.total_seconds()) #* replace it with response time from wiki server -> sleep untill response comes
        print(get)
        soup = bs(get.content, 'html.parser')
        self.comp_name = soup.find(class_='firstHeading').get_text()
        print(self.comp_name)
        try:
            get_table = soup.find('table', class_='infobox bordered')
            get_td = get_table.find_all('td')
            query_den_molar = ', '.join(list(i.get_text().strip(
            ) for i in get_td if 'g/mol' in i.get_text() or 'g·mol' in i.get_text() or 'g/cm' in i.get_text() or 'g/L' in i.get_text()))
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
        print('scraping has finished')
        return

    async def get_coeffs(self):  #*call as asyncio 
        print('get coeffs started')
        await asyncio.sleep(0.25)
        pattern = re.compile(r'([A-Z][a-z]?\d?)')
        res = re.findall(pattern, self.inp_comp)
        for n,i in enumerate(res):
            try:
                coeff = re.compile(r'[0-9]').search(i).group(0)
                self.coeffs.update({self.list_elems[n]:int(coeff)})
                print(i)
            except Exception as e:
                self.coeffs.update({self.list_elems[n]:1})
                print(e)
        if ')' in self.inp_comp:
            extra_coeff = int(re.compile(r'[0-9]$').search(self.inp_comp).group(0))
            iso_to_multi = set(list(self.coeffs.keys())).intersection(set(self.list_elems[1:]))
            self.coeffs.update({k:v*extra_coeff for k, v in self.coeffs.items() for i in iso_to_multi if k==i})
            # print(self.coeffs)

    @property
    def densities(self):
        comp_nucden = self.NA*self.comp_density/self.molar_mass
        self.nuc_dens.update({k: format(v*comp_nucden, '.4f')
                              for k, v in self.coeffs.items()})
        data_to_add = Call_comp().table(comp_name=self.comp_name, comp_formula=self.inp_comp,
                                        molar_mass=self.molar_mass, density=self.comp_density, nuclides=self.comp_nuclides, nuclides_as_elems=self.comp_elems, nuclear_densities=','.join(self.nuc_dens.values()))
        # Call_comp().add(data=data_to_add)  # * add to db
        return self.nuc_dens

# * template
# * input: formula like: UO2, NACl and so on
# * cols: ['comp_formula', 'comp_name','molar_mass', 'density', 'nuclides']


