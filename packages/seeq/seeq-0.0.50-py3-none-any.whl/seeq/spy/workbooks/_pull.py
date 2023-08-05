from .. import _common
from ._workbook import *


def pull(workbooks_df):
    results = list()
    for index, row in workbooks_df.iterrows():
        if not _common.present(row, 'ID'):
            raise RuntimeError('All rows in "workbooks" argument must have valid "ID" column')

        if _common.get(row, 'Type') == 'Folder':
            continue

        results.append(Item.pull(row['ID']))

    return results
