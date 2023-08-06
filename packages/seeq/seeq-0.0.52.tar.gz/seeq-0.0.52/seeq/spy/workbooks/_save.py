import os

from seeq.base import system


def save(workbooks, folder=None, *, clean=True):
    if folder is None:
        folder = os.getcwd()

    if clean:
        system.removetree(folder, keep_top_folder=True)

    for workbook in workbooks:
        workbook_folder_name = '%s (%s)' % (workbook.name, workbook.id)
        workbook_folder = os.path.join(folder, system.cleanse_filename(workbook_folder_name))
        workbook.save(workbook_folder)
