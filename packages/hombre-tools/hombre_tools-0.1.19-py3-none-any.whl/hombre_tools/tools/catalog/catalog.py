"""
Module fetchs JDE table catalog to pandas data frame
Stanislav Vohnik
2019-08-20
"""
from unicodedata import normalize
from pandas import read_html, DataFrame, concat
from requests_html import HTMLSession
from hombre_tools.utils.utils import run_in_separate_threads

def get_table_data(find, head, key, index=0, url='http://www.jdetables.com'):
    """
    response to dataframe
        parameters:
            url
            find string
            head: header 0/1
            key: index of a table on a html page
            index: index column
    """
    response = SESSION.get(url)
    table = response.html.find(find, first=False)[key].html
    data_frame = read_html(table, skiprows=0, header=head, index_col=index)[key]
    try:
        data_frame['Fk'] = f"{system}_{url.split('=')[-1]}"
        del data_frame["SQL Create Statement"]
        del data_frame['Unnamed: 0']
    except:
        pass
    return data_frame

TABLES = DataFrame()
COLUMNS = DataFrame()
SESSION = HTMLSession()

RESPONSE = SESSION.get('http://www.jdetables.com')
FIND = 'body > div.noprint select > option'
OPTIONS = RESPONSE.html.find(FIND, first=False)
SYSTEMS = [option.attrs['value'] for option in OPTIONS[1:]]
TITLES = [normalize("NFKD", code.full_text) for code in OPTIONS[1:]]

# test patameters
# SYSTEMS = ['01']
# TITLES = ['01: Address Book']

for e, system in enumerate(SYSTEMS):
    # getting tables for a system
    _find = 'body > div.middle > div.content > table'
    url = f'http://www.jdetables.com/?schema=920&system={system}'
    df = get_table_data(_find, 1, 0, url=url)
    tables = df.Table[:]
    df['system_name'] = TITLES[e]
    df['system'] = system
    TABLES = concat([TABLES, df])

    # getting table's columns within a system
    _find = 'body > div.middle form table'
    args = {"find":_find, "head":0, "key":0, "index":1}
    urls = [f'http://www.jdetables.com/?schema=920&system={system}&table={table}' for table in tables]
    print(f"{e+1}/{len(SYSTEMS)}, system_{system}, #tables: {len(tables)}")
    COLUMNS = concat([COLUMNS, run_in_separate_threads(urls, get_table_data, **args)])

"""You may need to save it into an excel files"""
# TABLES  # pandas frame with catalog
# TABLES.to_excel('jde_tables.xlsx')
# COLUMNS.to_excel('jde_columns.xlsx')
