import copy
from compounds_to_db import *
from call_db import *
import os
import datetime
import asyncio
from main import *


class Make_matr(PrepCals):
    def __init__(self):
        # self.inp_comp = 'Ba(NO3)2'
        # self.inp_comp = 'Fe2O3'
        # self.inp_comp = 'Al2O3'
        super().__init__()
        self.FILE_PATH = os.path.join(
            self.direc, 'input_mcu_file', 'matr-1465-crit')
        self.towrite_data = self.open(self.FILE_PATH)
        self.PEREODIC_TABLE = Call_PT().to_form_dic
        # self.inp_comp = inp_comp
        self.comp_db = Call_comp()
        self.add_todb = Comp_to_db(self.inp_comp, self.PEREODIC_TABLE)
    
    def make(self):
        self.identify()

    def identify(self):
        if len(self.inp_comp) < 3:
            self.nuc_dens = format(self.PEREODIC_TABLE[self.inp_comp][3], '.4f')
            print(self.nuc_dens)
        else:
            if not self.comp_db.check_exists(self.inp_comp):
                async def asy_main():
                    scrap = asyncio.create_task(self.add_todb.scrap_compoud())
                    get_nucl = asyncio.create_task(self.add_todb.get_nuclides())
                    await scrap
                    await get_nucl
                    return self.add_todb.densities
                self.nuc_dens=asyncio.run(asy_main())
            else:
                self.nuc_dens = self.comp_db.call_existing(self.inp_comp)
        return self.alter_file()

    @logging_decor
    def alter_file(self):
        pattern = str
        
        last_num = max((n, int(re.search(r'\d+', num).group()))
                        for n, num in enumerate(self.towrite_data) if not bool(num.find('MATR')))  #* tuple of (line,matr)
        pattern_num = f'MATR {last_num[1]+1},\n'
        if len(self.inp_comp) > 3:
            for k, v in self.nuc_dens.items():
                pattern += f'{k.upper()}  {v} / '
        else:
            pattern = f'{self.inp_comp.upper()}  {self.nuc_dens}'
        self.towrite_data.insert(last_num[0]+2, pattern_num)
        self.towrite_data.insert(last_num[0]+3, pattern)
        logger.debug(f'Material "{pattern_num[:-2]}" added')
        logger.debug(f'Nuclear density "{pattern}" added')
        # print(self.towrite_data)
        self.output('matr')
        # return Make_geom(self.inp_comp).make() #* must be run with as asyncio 

if __name__ == '__main__':
    # print(help(Make_matr()))
    # comp = input('Type compound: ')
    
    Make_matr().make() #* here will be instance argument

    # def nucl_dens(self):
