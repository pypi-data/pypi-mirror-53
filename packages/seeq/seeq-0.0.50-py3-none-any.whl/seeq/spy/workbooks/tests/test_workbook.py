import pytest

import pandas as pd

from seeq import spy

from ...tests import test_common


def setup_module():
    test_common.login()


@pytest.mark.disabled
def test_save_load():
    spy.login('mark.derbecker@seeq.com', 'SeeQ2013!')
    #workbooks = spy.workbooks.pull(pd.DataFrame([{'ID': 'D833DC83-9A38-48DE-BF45-EB787E9E8375'}]))
    #workbooks[0].save(r'D:\Scratch\WorkbookExport')

    workbook = spy.workbooks.load(r'D:\Scratch\WorkbookExport')
    workbook.push(prefix='crap')
