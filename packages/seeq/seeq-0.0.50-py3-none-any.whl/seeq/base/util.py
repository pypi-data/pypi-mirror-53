import re


def remove_regex_capture_group_names(regex):
    # PostgreSQL will choke on named capture groups
    return re.sub(r'\?<\w+>', '', regex)


def pythonize_regex_capture_group_names(regex):
    # Unlike standard regex syntax, Python capture groups have a capital P:  (?P<group_name>.*?)
    return re.sub(r'\?<(\w+)>', r'?P<\1>', regex)


def replace_tokens_in_regex(regex, group_dict):
    for name, value in group_dict.items():
        regex = regex.replace('${%s}' % name, re.escape(value))

    return regex
