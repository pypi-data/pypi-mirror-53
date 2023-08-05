"""Module for fetching metadata from database along with roe counts"""
from operator import itemgetter
from sqlalchemy import MetaData, create_engine, Table

METADATA = MetaData()
HOST = 'AWPJDEDB3'
DB = 'JDE_PROD_REP'
DRV = 'ODBC+Driver+13+for+SQL+Server'
MYPATH = 'c:/Users/stanislav_vohnik/Documents/JDE Queries Current'

TABLES = []
TABLES = {'F40344',}

ENGINE = create_engine(f'mssql+pyodbc://@{HOST}/{DB}?trusted_connection=yes&driver={DRV}')

for table in TABLES:
    _schema = table.split('.')
    if len(_schema) == 2:
        schema, name = _schema
    else:
        schema, name = 'PRODDTA', table
    print(f'{schema}.{name}')
    _ = Table(name, METADATA, autoload=True, autoload_with=ENGINE, schema=schema)

SQL = ' union all \n'.join([f"select '{key}' as name, count(*) from {key}"
                            for key in METADATA.tables.keys()])
CON = ENGINE.connect()
RESULT = sorted(CON.execute(SQL).fetchall(), key=itemgetter(1))
CON.close()

print('\n'.join([f'{e}, {key[0]}: {key[1]} x {len(METADATA.tables[key[0]].columns)}'
                 for e, key in enumerate(RESULT)]))

# print(enumerate(RESULT.keys())
