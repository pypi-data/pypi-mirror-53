"""
wraper for data profileing module
"""
import pandas_profiling as pp
from time import asctime
import re

def data_profile(data_frame, name, category='(_key$)|(_id$)|(_number$)'):
    dtype = {col:'category'
            for col in data_frame.columns
                    if isinstance(data_frame[col].values[0], str) or re.findall(category, col.lower())}

    print(asctime(), '\tProfileReport')
    data_frame=data_frame.astype(dtype)
    report = pp.ProfileReport(data_frame)

    report.to_file(f"{name}_report.html")
    print(asctime(), f'Done {name}')
