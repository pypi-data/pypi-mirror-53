# -*- coding: utf-8 -*-
"""Constants to use internally"""

#: directive name
DIRECTIVE_CHANGELOG = 'vcs_changelog'

#: option name to setup repo-path
OPTION_REPO_DIR = 'repo-path'

#: option name to select commits only after specified commit message or sha
OPTION_SINCE = 'added-since'

#: option name to take limited results count
OPTION_MAX_RESULTS_COUNT = 'limit'

#: option name to take commits if message matched regexp only
OPTION_MATCH = 'filter-regex'

#: option name to count commits if message matched regexp only
OPTION_MATCH_COUNT = 'context-regex-count'

#: option name to match regexp groups in commits
OPTION_MATCH_GROUPS = 'context-regex-groups'

#: option to define commit output template
OPTION_ITEM_TEMPLATE = 'item-template'

#: default commit output template is list item containing summary only
DEFAULT_ITEM_TEMPLATE_LIST = '{summary}'
DEFAULT_ITEM_TEMPLATE_TABLE = '"{summary}"'

#: option to define whole changelog output template
OPTION_LIST_TEMPLATE = 'list-template'

#: default changelog output template is list item containing summary only
DEFAULT_LIST_TEMPLATE = '{commits}'

OPTION_FORMAT = 'format'
OPTION_FORMAT_LIST = 'list'
OPTION_FORMAT_TABLE = 'table'
DEFAULT_FORMAT = OPTION_FORMAT_LIST

DEFAULT_TABLE_TEMPLATE = """
.. csv-table::
   {table_options}
   
{commits}
"""
LIST_ITEM_PREFIX = '- '
TABLE_ITEM_PREFIX = '   '

OPTION_TABLE_HEADER = 'table-header'
DEFAULT_TABLE_HEADER = '"What changed"'

OPTION_TABLE_CAPTION = 'table_caption'
DEFAULT_TABLE_CAPTION = "Changelog"


#: NOTSET value
NOTSET = object()

#: NOTSET str representation
NOTSET_STR = 'empty'

#: Known commit keys to use in templates
COMMIT_KEYS = [
    'message',
    'date',
    'author',
]
