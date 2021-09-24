import copy
from make_geom import Make_geom
from compounds_to_db import *
from call_db import *
import os
import datetime
from main import *


class Make_matr(PrepCals):
    def __init__(self):
        # self.inp_comp = 'Ba(NO3)2'
        # self.inp_comp = 'Fe2O3'
        # self.inp_comp = 'Al2O3'
        super().__init__()
        self.FILE_PATH = os.path.join(
            self.direc, 'input_mcu_file', 'matr-1465-crit')
        self.inp_comp = 'CaCO3'
        self.comp_db = Call_comp()

    def make(self):
        self.identify()

    def identify(self):
        pereodic_table = Call_PT().to_form_dic()
        if len(self.inp_comp) < 3:
            self.nuc_dens = pereodic_table[self.inp_comp][3]
            print(self.nuc_dens)
            return
        else:
            if not self.comp_db.check_exists(self.inp_comp):
                self.nuc_dens = Comp_to_db(
                    self.inp_comp, pereodic_table).get_nuclides()
            else:
                self.nuc_dens = self.comp_db.call_existing(self.inp_comp)
        return self.alter_file()

    def alter_file(self):
        pattern = str()
        self.towrite_data = self.open(self.FILE_PATH)
        last_num = max((n, int(re.search(r'\d+', num).group()))
                        for n, num in enumerate(self.towrite_data) if not bool(num.find('MATR')))  # * tuple of (line,matr)
        pattern_num = f'MATR {last_num[1]+1},\n'
        if len(self.nuc_dens) > 1:
            for k, v in self.nuc_dens.items():
                pattern += f'{k.upper()}  {v} / '

        self.towrite_data.insert(last_num[0]+2, pattern_num)
        self.towrite_data.insert(last_num[0]+3, pattern)
        # print(self.towrite_data)
        self.output('matr')
        # return Make_geom(self.inp_comp).make() #* must be run with as asyncio 

if __name__ == '__main__':
    # print(help(Make_matr()))
    Make_matr().make()

    # def nucl_dens(self):
