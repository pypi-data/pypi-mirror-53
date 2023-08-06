from .. import _common
from ._workbook import *


def pull(workbooks_df, *, include_referenced_workbooks=True):
    for required_column in ['ID', 'Type', 'Workbook Type']:
        if required_column not in workbooks_df.columns:
            raise RuntimeError('"%s" column must be included in workbooks_df' % required_column)

    results = list()
    workbooks_to_pull = dict()
    referencing_relative_path = dict()
    original_item_map = dict()
    for index, row in workbooks_df.iterrows():
        if _common.get(row, 'Type') == 'Folder':
            continue

        if _common.get(row, 'Workbook Type') == 'Analysis':
            if _common.get(row, 'ID') not in workbooks_to_pull:
                workbooks_to_pull[_common.get(row, 'ID')] = set()

            continue

        workbook = Item.pull(_common.get(row, 'ID'),
                             original_item_map=original_item_map,
                             allowed_types=['Workbook'])  # type: Workbook

        if include_referenced_workbooks and _common.get(row, 'Workbook Type') == 'Topic':
            for workbook_id, workstep_tuple in workbook.referenced_workbooks.items():
                if workbook_id not in workbooks_to_pull:
                    workbooks_to_pull[workbook_id] = set()

                if workstep_tuple not in workbooks_to_pull[workbook_id]:
                    workbooks_to_pull[workbook_id].update(workstep_tuple)
                    referencing_relative_path[workbook_id] = _common.get(row, 'Relative Path')

        if _common.present(row, 'Relative Path'):
            workbook['Relative Path'] = _common.get(row, 'Relative Path')

        results.append(workbook)

    for workbook_id, workstep_tuples in workbooks_to_pull.items():
        workbook = Item.pull(workbook_id,
                             original_item_map=original_item_map,
                             allowed_types=['Workbook'])  # type: Workbook

        workbook.pull_worksteps(list(workstep_tuples))

        workbook_row = workbooks_df[workbooks_df['ID'] == workbook_id]
        if len(workbook_row) == 1 and 'Relative Path' in workbook_row.columns:
            workbook['Relative Path'] = workbook_row.iloc[0]['Relative Path']
        elif workbook_id in referencing_relative_path and referencing_relative_path[workbook_id] is not None:
            # If the workbook was pulled only as a result of being referenced by something else (like a Topic),
            # we don't have a specific Relative Path to use. So just use the relative path of the referencing
            # item. (Note: If it's referenced by multiple things, then "last one wins".)
            workbook['Relative Path'] = referencing_relative_path[workbook_id]

        results.append(workbook)

    for workbook in results:
        workbook.use_original_ids(original_item_map)

    return results
