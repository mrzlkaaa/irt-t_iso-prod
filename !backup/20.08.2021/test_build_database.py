import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, select, delete
from sqlalchemy.orm import sessionmaker
import numpy as np
import psycopg2
# from examples.performance import Profiler
# from sqlalchemy.sql.sqltypes import Float






# *credentials
# SQL_USER = 'neug28'
PSQL_USER = 'admin'
SQL_PWD = 'gjyzif'
SQL_HOST = '109.123.162.3'
# SQL_DATABASE = 'isotopes_prod'
PSQL_DATABASE = 'test1'


# engine = create_engine(f'mysql+pymysql://{SQL_USER}:{SQL_PWD}@{SQL_HOST}/{SQL_DATABASE}', echo=True)
# * psql
engine = create_engine(f'postgresql://{PSQL_USER}:{SQL_PWD}@{SQL_HOST}:5433/{PSQL_DATABASE}', echo=True)
connection = engine.connect()
print(connection)
Base = declarative_base()

class MainTable(Base):
    __tablename__ = 'mainTable'
    id = Column(Integer, Sequence('id_seq'), primary_key=True) # *squence to generate values
    channel_name = Column(String(50))
    location = Column(String(100))
    diameter = Column(Float)
    height = Column(Float)
    ther_flux = Column(Float)
    epi_flux = Column(Float)
    fast_flux = Column(Float)
    uneven = Column(Float)
    

class NeutronicData44(Base):
    __tablename__ = 'neutronicData44'
    id = Column(Integer, Sequence('id_seq'), primary_key=True) # *squence to generate values
    energy44 = Column(Float)
    cec1_44 = Column(Float)
    # newchanl = Column(Float) #*todo find how add column to existing table

    def __repr__(self):
        return f'<Id: {self.id}, Energies: {self.energy44}, Flux: {self.cec1_44}>'

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
mySession = Session()



select = mySession.execute(select(NeutronicData44))
print(select.all())

mySession.commit() #* = must be used
mySession.close() #* = must be used or use <with>


table = NeutronicData44.__table__ #* get Table shema

# #! drop it
# print(table.drop(engine))
# print(type(table))


# def add():
    # return



# def add():
#     testadd = NeutronicData44(energy44=22)
#     mySession.add(testadd)
#     mySession.commit()

# add()
