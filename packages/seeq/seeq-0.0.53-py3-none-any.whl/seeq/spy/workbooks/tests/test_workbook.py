import pytest

from seeq import spy

from ...tests import test_common


def setup_module():
    # test_common.login()
    pass


@pytest.mark.system2
def test_save_load():
    spy.login(url='https://explore.seeq.com', username='mark.derbecker@seeq.com', password='RR!Harley',
              ignore_ssl_errors=True)

    # spy.login(username='mark.derbecker@seeq.com', password='SeeQ2013!')

    search_df = spy.workbooks.search({
        'ID': '51C5AAD6-AFED-4396-B84A-D06F65914503'
    }, content_filter='PUBLIC')

    #pull_df = spy.workbooks.pull(search_df[search_df['Name'].str.contains('Gothenburg')])
    #spy.workbooks.save(pull_df, r'D:\Scratch\WorkbookExport3')

    spy.login('mark.derbecker@seeq.com', 'SeeQ2013!', url='http://localhost:34216')

    pull_df = spy.workbooks.load(r'D:\Scratch\WorkbookExport3')
    status_df = spy.workbooks.push(pull_df, errors='catalog')

    # workbooks = spy.workbooks.load(r'D:\Scratch\WorkbookExport2')
    # spy.workbooks.push(workbooks)
