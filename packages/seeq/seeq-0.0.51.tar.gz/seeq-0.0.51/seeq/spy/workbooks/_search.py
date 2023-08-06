import json
import re
import requests

import pandas as pd

from seeq.sdk import *

from ...base import gconfig
from .. import _common
from .. import _login


def search(query, *, content_filter='owner', all_properties=False, recursive=False):
    return _search(query, content_filter, all_properties, recursive)


def _search(query, content_filter, all_properties, recursive, parent_id=None, parent_path='', root_path=None):
    items_api = ItemsApi(_login.client)
    users_api = UsersApi(_login.client)
    results_df = pd.DataFrame()

    for _key, _ in query.items():
        supported_query_fields = ['Path', 'Name', 'Description']
        if _key not in supported_query_fields:
            raise RuntimeError('"%s" unsupported query field, use instead one or more of: %s' %
                               (_key, ', '.join(supported_query_fields)))

    path_filter = query['Path'] if 'Path' in query else None

    path_filter_parts = list()
    if path_filter is not None:
        path_filter_parts = re.split(r'\s*>>\s*', path_filter.strip())

    if len(path_filter_parts) == 0 and root_path is None:
        root_path = parent_path

    if parent_id is not None:
        folder_output_list = _get_folders(content_filter=content_filter,
                                          folder_id=parent_id)
    else:
        folder_output_list = _get_folders(content_filter=content_filter)

    for content in folder_output_list['content']:
        path_matches = False
        props_match = True
        if content['type'] == 'Folder' and len(path_filter_parts) > 0 and \
                _common.does_query_fragment_match(path_filter_parts[0], content['name'], contains=False):
            path_matches = True

        for query_key, content_key in [('Name', 'name'), ('Description', 'description')]:
            if query_key in query and (content_key not in content or
                                       not _common.does_query_fragment_match(query[query_key],
                                                                             content[content_key])):
                props_match = False
                break

        absolute_path = parent_path
        relative_path = absolute_path
        if root_path is not None:
            relative_path = parent_path[len(root_path):]
            if relative_path.startswith(' >> '):
                relative_path = relative_path[4:]

        if props_match and len(path_filter_parts) == 0:
            if 'username' in content['owner']:
                owner_username = content['owner']['username']
            else:
                user_output = users_api.get_user(id=content['owner']['id'])  # type: UserOutputV1
                owner_username = user_output.username

            content_dict = {
                'ID': content['id'],
                'Type': content['type'],
                'Path': absolute_path,
                'Relative Path': relative_path,
                'Name': content['name'],
                'Owner Name': content['owner']['name'],
                'Owner Username': owner_username,
                'Owner ID': content['owner']['id'],
                'Pinned': content['markedAsFavorite'],
                'Created At': pd.to_datetime(content['createdAt']),
                'Updated At': pd.to_datetime(content['updatedAt']),
                'Access Level': content['accessLevel']
            }

            if content['type'] != 'Folder':
                content_dict['Workbook Type'] = _common.get_workbook_type(content['data'])

            if all_properties:
                excluded_properties = [
                    # Exclude these because they're in ns-since-epoch when we retrieve them this way
                    'Created At', 'Updated At',

                    # Exclude this because it's a bunch of JSON that will clutter up the DataFrame
                    'Data', 'workbookState'
                ]

                _item = items_api.get_item_and_all_properties(id=content['id'])  # type: ItemOutputV1
                for prop in _item.properties:  # type: PropertyOutputV1

                    if prop.name in excluded_properties:
                        continue

                    content_dict[prop.name] = _common.none_to_nan(prop.value)

            results_df = results_df.append(content_dict, ignore_index=True)

        if content['type'] == 'Folder' and ((recursive and len(path_filter_parts) == 0) or path_matches):
            child_path_filter = None
            if path_filter_parts and len(path_filter_parts) > 1:
                child_path_filter = ' >> '.join(path_filter_parts[1:])

            if len(parent_path) == 0:
                new_parent_path = content['name']
            else:
                new_parent_path = parent_path + ' >> ' + content['name']

            child_query = dict(query)
            if not child_path_filter and 'Path' in child_query:
                del child_query['Path']
            else:
                child_query['Path'] = child_path_filter

            child_results_df = _search(child_query, content_filter, all_properties, recursive, content['id'],
                                       new_parent_path, root_path=root_path)

            results_df = results_df.append(child_results_df, ignore_index=True)

    return results_df


def _get_folders(content_filter='ALL', folder_id=None, archived=False, sort_order='createdAt ASC', only_pinned=False):
    # We have to make a "raw" REST request here because the get_folders API doesn't work well due to the
    # way it uses inheritance.
    api_client_url = gconfig.get_api_url()
    query_params = 'filter=%s&isArchived=%s&sortOrder=%s&limit=100000&onlyPinned=%s' % (
        content_filter,
        str(archived).lower(),
        sort_order,
        str(only_pinned).lower())

    request_url = api_client_url + '/folders?' + query_params

    if folder_id:
        request_url += '&folderId=' + folder_id

    response = requests.get(request_url, headers={
        "Accept": "application/vnd.seeq.v1+json",
        "x-sq-auth": _login.client.auth_token
    }, verify=Configuration().verify_ssl)

    return json.loads(response.content)
