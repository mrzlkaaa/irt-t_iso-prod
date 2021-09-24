import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, select, delete
from sqlalchemy.orm import sessionmaker, Session
import numpy as np
import psycopg2

# from compounds_to_db import *
# from examples.performance import Profiler
# from sqlalchemy.sql.sqltypes import Float


# *credentials
PSQL_USER = 'admin'
PSQL_PWD = 'gjyzif'
PSQL_HOST = '109.123.162.3'
PSQL_PORT = '5433'
PSQL_DATABASE = 'iso_prod'

# * psql
engine = create_engine(
    f'postgresql://{PSQL_USER}:{PSQL_PWD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}', echo=False)
connection = engine.connect()
print(connection)
Base = declarative_base()


class Compounds(Base):
    __tablename__ = 'compounds'
    # *squence to generate values
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    comp_name = Column(String(100))
    comp_formula = Column(String(50))
    molar_mass = Column(Float)
    density = Column(Float)
    nuclides = Column(String(200))
    nuclides_as_elems = Column(String(100))

# Base.metadata.create_all(engine)


# Session = sessionmaker(bind=engine)
# mySession = Session()

# select = mySession.execute(text('SELECT * FROM pereodic_table')).all()
# print(select)
# # select = mySession.execute(select(PereodicTable))
# # print(select.all())

# mySession.commit() #* = must be used
# mySession.close() #* = must be used or use <with>


# table = NeutronicData44.__table__ #* get Table shema

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
