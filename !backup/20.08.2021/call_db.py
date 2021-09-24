from sqlalchemy.sql.schema import MetaData
from sqlalchemy import *
from build_database import *

# * engine from build_database.py


class Call_db:
    # def __init__(self):
    #     self.pereodic_table = 'pereodic_table'
    def call(self):
        with Session(engine) as session:
            response = session.execute(
                text(f'SELECT * FROM {self.table}')).all()  # * list
            # print(response)
            return response
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
                                  self.table.nuclides).all()

    def call_existing(self, formula):
        response = self.session.query(self.table.id, self.table.comp_name, self.table.comp_formula, self.table.molar_mass, self.table.density,
                                      self.table.nuclides).where(self.table.comp_formula == formula).first()
        return [response[3], response[4], response[5]]

    def check_exists(self, inp_comp):
        return bool([i for i in self.session.query(self.table.comp_formula) if inp_comp in i[0]])

    def add(self, *args, **kwargs):
        self.session.add(kwargs['data'])
        self.session.commit()
    # def add(self):


if __name__ == '__main__':
    Call_mcu().call()
    Call_comp().call()
