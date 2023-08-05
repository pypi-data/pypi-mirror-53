"""
Example of connecting to edvards oracle instance
Stanislav Vohnik 2019-08-21
"""
from os import environ
from sqlalchemy import create_engine, exc
from keyring import get_password as pswd
import logging
from pandas import DataFrame, read_sql

def ora_url(args):
    return f'oracle://{args.user}:{pswd(args.host, args.user)}@{args.host}/{args.sid}'

def mssql_url(args, drv='ODBC+Driver+13+for+SQL+Server'):
    return f'mssql+pyodbc://@{args.host}/{args.db}?trusted_connection=yes&driver={drv}'

def sqlalchemy_engine(args, url):
    """engine constructor"""
    environ['PATH'] = args.ora_path  # we have to point to oracle client directory
    url = f'oracle://{args.user}:{pswd(args.host, args.user)}@{args.host}/{args.sid}'
    logging.info(url)
    return create_engine(url) # SQL Alchemy Engine

def get_ora_tables(engine):
    """wrapper for pandas read_sql returns data frame 'select * from all_tables' """
    sql = 'select * from all_tables'
    return read_sql(engine, sql)

def db_read_sql(engine, sql):
    """wrapper for pandas read_sql returns data frame"""
    data_frame = DataFrame()
    print(engine)
    try:
        with engine.connect() as con:
            data_frame = read_sql(sql, con)
    except exc.DatabaseError as msg:
        logging.error(msg)
    return data_frame # Pandas DataFrame