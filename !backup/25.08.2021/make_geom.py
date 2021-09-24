import re
from statistics import mean
from collections import Counter
from main import *

count = Counter()


class Make_geom(PrepCals):
    def __init__(self, inp_comp):
        super().__init__()
        self.FILE_PATH = os.path.join(
            self.direc, 'input_mcu_file', 'geom_be_tvs_6layer_10.12.2018')
        self.inp_comp = inp_comp
        self.CH_NAME = 'CEC1'
        self.MAX_RAD = 2
        self.MIN_MAX_h = [-4, 62]
        self.height = self.exception(float(input('Type height of sample: ')), self.MIN_MAX_h[1], self.MIN_MAX_h[0])
        self.radius = self.exception(float(input('Type radius of sample: ')), self.MAX_RAD)

    def make(self):
        self.alter_file()

    def exception(self, value, max_value, min_value=None):
        if min_value is None:
            if value <= max_value:
                return value
            else:
                return self.exception(float(input(f'type value that smaller of equal to {max_value} ')), max_value)
        else:
            if min_value <= value <= max_value:
                return value
            else:
                return self.exception(float(input(f'type value that smaller or equal to {max_value} / bigger or equal to {min_value} ')), max_value, min_value)

    def set_h(self):
        return mean(self.MIN_MAX_h)-self.height/2
    
    def parse_block(self):
        get_pos = ((n, i) for n, i in enumerate(
            self.towrite_data, start=1) if self.CH_NAME in i)  #* get the specific geom block starting line
        self.starting_line = next(get_pos)[0]
        get_range = ((n, i) for n, i in enumerate(
            self.towrite_data[self.starting_line:], start=1) if 'END' in i or 'ENDL' in i)
        self.finish_line_g = next(get_range)[0].__add__(self.starting_line)
        return self.towrite_data[self.starting_line: self.finish_line_g]
    
    def alter_file(self):
        drop_nums = re.search(r"\D+", self.inp_comp).group().upper()
        pattern = f'RCZ {drop_nums} 0,0,{self.set_h()} {self.height} {self.radius}\n'
        self.towrite_data = self.open(self.FILE_PATH)
        block = self.parse_block()
        for n, i in enumerate(block):
            if i.startswith('\n'):
                count.update('+')  # *count of lines that added
                self.towrite_data.insert(n+self.starting_line, pattern)
        # print(self.towrite_data[self.starting_line:self.finish_line_g+len(count)])
        self.output('geom')
        return

#! add oprion to add a bunch of geometry objects

# if __name__ == '__main__':
#     Make_geom('CaCO3').make()
