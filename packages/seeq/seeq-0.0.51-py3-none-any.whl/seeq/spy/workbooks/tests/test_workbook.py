import pytest

from seeq import spy

from ...tests import test_common


def setup_module():
    test_common.login()


@pytest.mark.system2
def test_save_load():
    spy.login('mark.derbecker@seeq.com', 'SeeQ2013!')

    search_df = spy.workbooks.search({
        'Path': 'My Import'
    }, recursive=True)

    workbooks = spy.workbooks.pull(search_df)
    spy.workbooks.save(workbooks, r'D:\Scratch\WorkbookExport2', clean=True)

    #workbooks = spy.workbooks.load(r'D:\Scratch\WorkbookExport')
    #spy.workbooks.push(workbooks, path='This >> Cool', label='Markus')
