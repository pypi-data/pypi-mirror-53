"""
For each line with JDE table or
column object adds comment with JDE object description
Stanislav Vohnik
2019-09-06
"""
import re
from os import path
from pandas import HDFStore, DataFrame

# RAEDING JDE CATALOG
with HDFStore('/'.join(path.realpath(__file__).split('\\')[:-1]) +'/catalog/catalog_new.h5') as store:
    print(store.info())
    TABLES = store.get('tables')
    COLUMNS = store.get('columns')

CATALOG = ((TABLES, 'Table'),
           (COLUMNS, 'Field'))

OPTIONS = {'keyword_case':'upper',
           'reindent':True,
           'indent_width':4}

P = re.compile(r'(\w*)')

STOP_WORD = {'', 'select', 'from', 'as', 'where', 'group', 'by',
             'left', 'join', 'is', 'not', 'null', 'inner',
             'outer', 'case', 'when', 'else', 'then', 'end',
             'union', 'nolock', 'in', 'order'}

#creating index to speed _find
TABLES.reset_index()
TABLES.set_index('Table', inplace=True)
COLUMNS.reset_index()
COLUMNS.set_index('Field', inplace=True)

def _find(catalog, word):
    """
    finds description by df index
    """
    descr = None
    if word.lower() in STOP_WORD:
        return None
    try:
        if isinstance(catalog.loc[word], DataFrame):
            descr = catalog.loc[word].Description.any()
        else:
            descr = catalog.loc[word].Description

    except (AttributeError, KeyError):
        pass
    return descr

def comment(script):
    """
    For each line with JDE table or
    column adds comment with JDE object description
    """
    sqls = []
    for sql in script.split(';'):
        lines = []
        for line in sql.splitlines():
            if '*/' in line:
                continue
            _comment = []
            for word in P.findall(line):
                for _catalog, _ in CATALOG:
                    descr = _find(_catalog, word)
                    if descr:
                        _comment.append(f'{word}:{descr}')
            if _comment:
                line += f" /* {', '.join(_comment)} */"
            lines.append(line)
        sqls.append('\n'.join(lines[:]))
    return ';\n'.join(sqls)
