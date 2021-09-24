from sqlalchemy.sql.schema import MetaData
from sqlalchemy import *
from build_database import *

# * engine from build_database.py


class Call_db:
    def __init__(self):
        self.response = tuple()

    def call(self):
        with Session(engine) as session:
            self.response = session.execute(
                text(f'SELECT * FROM {self.table}')).all()  # * list
            return self.response
    # def add_db(self):


# * call for mcu_db
class Call_mcu(Call_db):
    def __init__(self):
        super().__init__()
        self.table = 'mcu_iso'

# * call for pt


class Call_PT(Call_db):
    def __init__(self):
        super().__init__()
        self.table = 'pereodic_table'

    def to_form_dic(self):
        return {i[2]: [i[1], i[3], i[4], i[5]] for i in self.call()}


# * call for compounds


class Call_comp(Call_db):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.table = Compounds
        self.session = self.run_session()

    def run_session(self):
        with Session(engine) as session:
            return session

    def call(self):
        return self.session.query(self.table.id, self.table.comp_name, self.table.comp_formula, self.table.molar_mass, self.table.density,
                                  self.table.nuclides, self.table.nuclear_densities).all()

    def call_existing(self, formula):
        response = self.session.query(self.table.id, self.table.comp_name, self.table.comp_formula, self.table.molar_mass, self.table.density,
                                      self.table.nuclides, self.table.nuclides_as_elems, self.table.nuclear_densities).where(self.table.comp_formula == formula).first()
        return {k:v for k,v in zip(response[6].split(','), response[7].split(','))}

    def check_exists(self, inp_comp):
        return bool([i for i in self.session.query(self.table.comp_formula) if inp_comp in i[0]])

    def add(self, *args, **kwargs):
        self.session.add(kwargs['data'])
        self.session.commit()
    # def add(self):


if __name__ == '__main__':
    Call_mcu().call()
    Call_comp().call()
