import json
import re
import requests

import pandas as pd
import numpy as np

from seeq.sdk import *

from ...base import gconfig
from .. import _common
from .. import _login


class Workbook:
    pass


class Analysis(Workbook):
    pass


def search(path=None, content_filter='owner', all_properties=False, recursive=False):
    return _search(path, content_filter, all_properties, recursive)


def _search(path_filter, content_filter, all_properties, recursive, parent_id=None, parent_path=None,
            original_path_filter=None):
    items_api = ItemsApi(_login.client)
    users_api = UsersApi(_login.client)
    results_df = pd.DataFrame()

    path_filter_parts = None
    if path_filter is not None:
        path_filter_parts = re.split(r'\s*>>\s*', path_filter.strip())

    if parent_id is not None:
        folder_output_list = _get_folders(content_filter=content_filter,
                                          folder_id=parent_id)
    else:
        folder_output_list = _get_folders(content_filter=content_filter)

    for content in folder_output_list['content']:
        if path_filter_parts and content['name'] != path_filter_parts[0]:
            continue

        absolute_path = parent_path if parent_path else ''
        relative_path = absolute_path
        if original_path_filter is not None:
            relative_path = parent_path[len(original_path_filter):]
            if relative_path.startswith(' >> '):
                relative_path = relative_path[4:]
        else:
            original_path_filter = path_filter

        if not path_filter_parts:
            if 'username' in content['owner']:
                owner_username = content['owner']['username']
            else:
                user_output = users_api.get_user(id=content['owner']['id'])  # type: UserOutputV1
                owner_username = user_output.username

            content_dict = {
                'ID': content['id'],
                'Type': content['type'],
                'Absolute Path': absolute_path,
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

        if content['type'] == 'Folder' and recursive:
            child_path_filter = None
            if path_filter_parts and len(path_filter_parts) > 1:
                child_path_filter = ' >> '.join(path_filter_parts[1:])

            if parent_path is None:
                new_parent_path = content['name']
            else:
                new_parent_path = parent_path + ' >> ' + content['name']

            child_results_df = _search(child_path_filter, content_filter, all_properties, recursive, content['id'],
                                       new_parent_path, original_path_filter=original_path_filter)

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
