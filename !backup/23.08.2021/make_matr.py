import copy
from compounds_to_db import *
from call_db import *
import os


class Make_matr:
    def __init__(self):
        # self.inp_comp = 'Ba(NO3)2'
        # self.inp_comp = 'Fe2O3'
        self.inp_comp = 'TeO2'
        self.comp_db = Call_comp()
        self.molar_mass = float()
        self.comp_density = float()
        self.comp_nuclides = str()
        self.comp_elems = str()
        self.coeffs = {}
        self.nuc_dens = {}
        self.NA = 0.602

    def make(self):
        self.identify()
        self.get_coeffs()
        self.densities()

    def densities(self):
        comp_nucden = self.NA*self.comp_density/self.molar_mass
        self.nuc_dens.update({k:format(v*comp_nucden, '.4f') for k,v in self.coeffs.items()})
        print(self.nuc_dens)

    def identify(self):
        pereodic_table = Call_PT().to_form_dic()
        if len(self.inp_comp) < 3:
            elem, self.molar_mass, self.comp_density = pereodic_table[self.inp_comp][
                0], pereodic_table[self.inp_comp][1], pereodic_table[self.inp_comp][2]
        else:
            if not self.comp_db.check_exists(self.inp_comp):
                self.molar_mass, self.comp_density, self.comp_nuclides, self.comp_elems = Comp_to_db(
                    self.inp_comp, pereodic_table).get_nuclides()
            else:
                self.molar_mass, self.comp_density, self.comp_nuclides, self.comp_elems = self.comp_db.call_existing(
                    self.inp_comp)
        return

    def get_coeffs(self):
        pattern = re.compile(r'\d')
        res = pattern.finditer(self.inp_comp)

        for v in res:
            if self.inp_comp[v.span()[0]-1] != ')' and self.inp_comp[v.span()[0]-1].islower()==False:
                self.coeffs.update({self.inp_comp[v.span()[0]-1]: int(self.inp_comp[v.span()[0]])})
                print(self.inp_comp[v.span()[0]-1].islower())
            elif self.inp_comp[v.span()[0]-1] != ')' and self.inp_comp[v.span()[0]-1].islower():
                self.coeffs.update({self.inp_comp[v.span()[0]-2:v.span()[0]]: int(self.inp_comp[v.span()[0]])})
        print(self.coeffs)
        elems_got_coefs = copy.copy(self.coeffs)
        print(self.comp_elems.split(','))
        self.coeffs.update({j: 1 for j in self.comp_elems.split(
            ',') if j not in ''.join(elems_got_coefs.keys())})
        print(self.coeffs)
        if '(' in self.inp_comp:
            pattern_with_parh = re.compile(r'[(]\w+[)]\w+')
            parh_match = pattern_with_parh.search(self.inp_comp)
            matches = parh_match.group()
            multi_coef = int(matches[-1:])
            up_on_multi = {k: v*multi_coef for k, v in self.coeffs.items()
                           if k in matches}
            self.coeffs.update(up_on_multi)
            print(self.coeffs)
            return self.coeffs
        else:
            return self.coeffs


if __name__ == '__main__':
    Make_matr().make()
    # def nucl_dens(self):
