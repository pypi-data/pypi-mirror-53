"""Main module for comand line usege of hombre_tools"""
from os import scandir
import logging
import sqlparse
from hombre_tools.utils.utils import argument_parser

def jde_comment():
    """ adds comment to JDE source queries"""
    from hombre_tools.tools.jde_sql_decorate import comment as _comment, OPTIONS
    print(ARGS.path)
    OPTIONS['strip_comments'] = ARGS.strip_comments
    header = ARGS.header
    _copyright = f'Copyright Edwards Lifesciences {ARGS.year}, All rights reserved.'
    author = ARGS.author
    path = ARGS.path

    files = [entry for entry in scandir(path) if entry.is_file()]

    for file in files:
        with open(file.path) as in_file:
            print(file.path)
            new_name = file.path.split('.')[0] + '.sql'
            script = sqlparse.format(in_file.read(), **OPTIONS)
            _header = ['/*',
                       f'/*\n{_copyright}',
                       f'AUTHOR:{author}',
                       f'{header}',
                       f'file_name: {file.name.split(".")[0] +".sql"}',
                       '*/\n']
            
            header = '\n'.join(_header)
            script = header + _comment(script)
            new_name = file.path.split('.')[0] + '.sql'
            with open(new_name, 'w') as out_file:
                out_file.write(script)

def profile():
    """wrapper for data profile module"""
    from hombre_tools.db.db import sqlalchemy_engine, db_read_sql, ora_url
    from hombre_tools.tools.data_profiling import data_profile
    url = ora_url(ARGS) # TODO via
    engine = sqlalchemy_engine(ARGS,url)
    data_frame = db_read_sql(engine, ARGS.sql)
    ARGS.data_frame = data_frame
    if not data_frame.empty:
        data_profile(data_frame, ARGS.name, category=ARGS.category)
    else:
        logging.warning('No data')
            

if __name__ == '__main__':
    try:
        PARSER = argument_parser()
        ARGS = PARSER.parse_args()
        ACTION = ARGS.action
        globals()[ACTION]()
    except KeyError as msg:
        print(f'Error action  {msg} is not defined')
    
    print('Done')
