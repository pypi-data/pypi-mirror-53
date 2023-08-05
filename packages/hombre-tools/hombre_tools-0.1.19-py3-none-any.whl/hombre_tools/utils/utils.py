'''
set of tools utilites
'''
import concurrent.futures
import logging
from argparse import ArgumentTypeError, ArgumentParser
from pandas import DataFrame, concat as pd_concat


def str2bool(answer):
    """function for argparse to validate boolean input"""
    if answer.lower() in ('yes', 'true', 't', 'y', '1'):
        result = True
    elif answer.lower() in ('no', 'false', 'f', 'n', '0'):
        result = False
    else:
        raise ArgumentTypeError("Boolean value expected.")
    return result

def argument_parser(description='tools cmd'):
    """Common set of arguments for CMD tools"""
    description = '''Hombre tools\n\r
       Examples: \n\r
                python -m hombre_tools --action profile --sql "select * from dim_country" --user xxxx --host host --sid sid --name nameit\n\r
                python -m hombre_tools --action jde_comment  --path "C:/Queries"'''
    
    parser = ArgumentParser(description=description)

    parser.add_argument("--login",
                        help='db login',
                        required=False)

    parser.add_argument("--host",
                        required=False,
                        help='uri of host')

    parser.add_argument("--path",
                        default=None,
                        required=False)

    parser.add_argument("--strip_comments",
                        const=False,
                        default=False,
                        type=str2bool,
                        nargs='?',
                        required=False,
                        help="If True existing comments are removed from the statements")

    parser.add_argument("--author", default='', required=False)

    parser.add_argument("--header", default='JDE Queries', required=False)

    parser.add_argument("--year", default='2019', required=False)

    parser.add_argument("--action", required=False, help='jde_comment, profile')


    parser.add_argument("--category",
                        required=False,
                        default='(_key$)|(_id$)|(_number$)')

    parser.add_argument("--name", required=False)

    parser.add_argument("--sql", required=False)

    parser.add_argument("--user", required=False)

    parser.add_argument("--ora_path",
                        required=False,
                        default='C:/oracle/instantclient;%PATH%')

    parser.add_argument("--sid", required=False)


    return parser

def max_lenght(data_frame, col):
    '''returns leghth of fdataframe object'''
    return max(len(data_frame[col].astype(str).min()), len(data_frame[col].astype(str).max())) + 1


def run_in_separate_threads(items, target, **args):
    """Wrapper to execute method in separate tread
    for each "item" and concat them into DataFrame."""
    _result = DataFrame()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_result = {executor.submit(target, *list(args.values()) + [item]):\
                         e for e, item in enumerate(items)}
        for future in concurrent.futures.as_completed(future_result):
            try:
                data = future.result()
            except (ValueError, AttributeError) as exc:
                logging.warning(' %s generated an exception: %s', target.__name__, exc)
                data = DataFrame()

            _result = pd_concat([_result, data])

    return _result
