"""
Example of connecting to edwards  instance
Stanislav Vohnik 2019-08-21
"""
from pandas import read_sql
from  pandas_profiling import ProfileReport
from sqlalchemy import create_engine

HOST = 'AWPJDEDB3'
DB = 'JDE_PROD_REP'
DRIVER = 'ODBC+Driver+13+for+SQL+Server'
URL = f'mssql+pyodbc://@{HOST}/{DB}?trusted_connection=yes&driver={DRIVER}'

EMGINE = create_engine(URL)

TABLES = ['PRODDTA.F0025',
        'PRODDTA.F0013',
        'PRODDTA.F40205',
        'PRODDTA.F0010',
        'PRODDTA.F1113',
        'PRODDTA.F55XLVL2',
        'PRODDTA.F5541JP1',
        'PRODDTA.F0006',
        'PRODDTA.F01151',
        'PRODDTA.F4101D',
        'PRODDTA.F0007',
        'PRODDTA.F554701']

for table in  TABLES:
    df = read_sql(f"select * from {table}", EMGINE)
    report = ProfileReport(df)
    
    for col in df.filter(regex='^ID').columns:
        df[col] = df[col].astype('categorical')
    report.to_file(f'{table}_profile.html')
   
    print(f'saved: {table}')

# import HPFS5
# comand = 'bcp JDE_PROD_REP.PRODCTL.F0101 out F0101.csv  -b format -c'
# '''https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-2017'''
