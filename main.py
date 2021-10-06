import os, sys
import concurrent.futures
import datetime
import copy
import asyncio
import re
import logging
import datetime
from statistics import mean
from collections import Counter, defaultdict
from compounds_to_db import *
from call_db import *

# from shapes_predictor.draw import Predict #comment it out for home_linux

count = Counter()
logger = logging.getLogger(__name__)
PATH = os.path.join(os.getcwd(), 'output_mcu', logger.name)
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
file_str = logging.FileHandler(f'{PATH}')
logger.addHandler(file_str)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_str.setFormatter(formatter)

def logging_decor(func):
    print(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Function "{func.__name__}" ran')
        func(*args, **kwargs)
    return wrapper

class PrepCals:
    def __init__(self, *args, **kwargs):
        self.direc = os.getcwd()
        self.pth_burn = os.path.join(self.direc, 'input_mcu_file', 'burn')
        self.output_folder = os.path.join(self.direc, 'output_mcu')
        self.towrite_data = list()

    def open(self, path):
        with open(path, 'r', encoding='latin-1') as fl:
            return fl.readlines()
            # return (i for i in fl.readlines())
    
    @logging_decor
    def output(self, file_name):
        set_path = os.path.join(
            self.output_folder, f'{self.inp_comp}_{datetime.date.today()}')
        if not os.path.exists(set_path):
            os.makedirs(set_path)
        to_save_path = os.path.join(set_path, file_name)
        logger.info(f'Saving path is "{set_path}" where "{file_name}" created successfully')
        # print(to_save_path)
        with open(to_save_path, 'w',  encoding='latin-1') as out:
            out.writelines(self.towrite_data)


class Make_matr(PrepCals):
    test = 'testarg'
    def __init__(self, *args, **kwargs):
        # self.inp_comp = 'Ba(NO3)2'
        # self.inp_comp = 'Fe2O3'
        # self.inp_comp = 'Al2O3'
        super().__init__(*args, **kwargs)
        self.inp_comp = kwargs['input']
        self.FILE_PATH = os.path.join(
            self.direc, 'input_mcu_file', 'matr-1465-crit')
        self.towrite_data = self.open(self.FILE_PATH)
        print(sys.getsizeof(self.towrite_data))
        self.PEREODIC_TABLE = Call_PT().to_form_dic
        self.comp_db = Call_comp()
        self.add_todb = Comp_to_db(self.inp_comp, self.PEREODIC_TABLE)
    
    def make(self):
        logger.info(f'has started with {self.__class__.__name__} in {datetime.datetime.now()}')
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
        pattern = str()
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
        logger.info(f'Material "{pattern_num[:-2]}" added')
        logger.debug(f'Nuclear density "{pattern}" added')
        # print(self.towrite_data)
        # self.output('matr')


class Make_geom(PrepCals):
    MAX_RAD = 2 #* will be dynamic corresponding with CH_NAME
    MIN_MAX_h = [-4, 62] #* will be dynamic corresponding with CH_NAME
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inp_comp = kwargs['input']
        self.height = self.exception(kwargs['height'], self.MIN_MAX_h[1], self.MIN_MAX_h[0])
        self.radius = self.exception(kwargs['radius'], self.MAX_RAD)
        self.sample_parts = kwargs['sample_parts']
        self.radius_devision = kwargs['radius_devision'] #boolean
        self.FILE_PATH = os.path.join(
            self.direc, 'input_mcu_file', 'geom_be_tvs_6layer_10.12.2018')
        self.towrite_data = self.open(self.FILE_PATH)  # * open file and grap all content
        self.CH_NAME = 'CEC1' #* will be dynamic

    def exception(self, value, max_value, min_value=None):
        if min_value is None:
            response = value if 0 < value <= max_value else self.exception(float(input(f'type value that smaller of equal to {max_value} ')), max_value)
            return response
        else:
            response = value if min_value <= value <= max_value else self.exception(float(input(f'type value that smaller or equal to {max_value} / bigger or equal to {min_value} ')), max_value, min_value)
            return response 
                
    @property
    def set_h(self):
        return mean(list(map(abs, self.MIN_MAX_h)))-self.height/2
    
    def set_r(self, radius, parts):
        radius-=self.radius/parts
        return radius
    
    def value_formatter(self, value):
        return format(value, ".3f")

    def pull_log_data(self):
        return

    @property
    def loop_text_block(self):
        positions = defaultdict(tuple)
        for n,i in enumerate(self.towrite_data, start=1):
            if self.CH_NAME in i:
                positions['start'] += (n,i)
            elif 'ENDL' in i and len(positions) > 0:
                positions['end'] += (n,i)
                break
        return self.towrite_data[positions['start'][0]: positions['end'][0]], positions['start'][0], positions['end'][0]

    @logging_decor
    def modify_file(self):
        pattern = str()
        drop_nums = ''.join(re.findall(r"[^()0-9]+", self.inp_comp)).upper()
        # self.rad_parts = Predict().predict if self.radius_devision else 1  #comment it out for home_linux
        self.rad_parts = 3
        for i in range(1, self.sample_parts+1):
            for j in range(1, self.rad_parts+1):
                pattern += f'RCZ {drop_nums}{i}{j} 0,0,{self.value_formatter(self.set_h+(self.height/self.sample_parts)*i)} {self.value_formatter(self.height/self.sample_parts)} \
                            {self.value_formatter(self.radius - self.set_r(self.radius, j))}\n'
        #TODO take matr number from .log file
        print(pattern)
        block, start, end = self.loop_text_block
        for n, i in enumerate(block):
            if i.startswith('\n'): self.towrite_data.insert(n+start, pattern)
        # logger.debug(f'Body "{pattern}" has added in block from line "{start}"')
        # self.output('geom')
        return

#! add oprion to add a bunch of geometry objects
#TODO combine with shape prediction model and drawing tool 

if __name__ == '__main__':
    comp = 'TeO2'
    while True:
        try:
            height = 10
            radius = 2
            sample_parts = 5
            radius_devision = True
            # height = float(input('Type height of sample: '))
            # radius = float(input('Type radius of sample: '))
            # sample_parts = int(input('Type on how many parts divide body: '))
            # radius_devision = True if input('Is radius division required? ').upper() == 'Y' else False
            break
        except ValueError as ve:
            print(ve)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        r1 = executor.submit(Make_matr(input=comp).make())
        r2 = executor.submit(Make_geom(input=comp, height=height, radius=radius, sample_parts=sample_parts, radius_devision=radius_devision).modify_file())
# # PrepCals(input=comp)
# Make_matr(input=comp).make()
# Make_geom(input=comp).make()


