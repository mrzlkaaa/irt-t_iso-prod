from compounds_to_db import *
from call_db import *


class Make_matr():
    def __init__(self):
        self.inp = 'CaCO3'
        self.molar_mass, self.comp_density, self.comp_nuclides = self.comp_db.call_existing(
                    self.inp_comp)
    