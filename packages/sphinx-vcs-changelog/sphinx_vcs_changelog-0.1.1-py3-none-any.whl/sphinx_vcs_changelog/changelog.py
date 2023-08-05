# -*- coding: utf-8 -*-
"""Simple linear changelog"""
#
#  Copyright 2018-2019 (C) Aleksey Marin <asmadews@gmail.com>
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from datetime import datetime

from docutils.frontend import OptionParser
from docutils.io import StringInput
from git import Commit
from sphinx_vcs_changelog.constants import DEFAULT_FORMAT
from sphinx_vcs_changelog.constants import DEFAULT_ITEM_TEMPLATE_TABLE

from sphinx_vcs_changelog.constants import DEFAULT_LIST_TEMPLATE
from sphinx_vcs_changelog.constants import DEFAULT_ITEM_TEMPLATE_LIST
from sphinx_vcs_changelog.constants import DEFAULT_TABLE_CAPTION
from sphinx_vcs_changelog.constants import DEFAULT_TABLE_HEADER
from sphinx_vcs_changelog.constants import DEFAULT_TABLE_TEMPLATE
from sphinx_vcs_changelog.constants import LIST_ITEM_PREFIX
from sphinx_vcs_changelog.constants import NOTSET
from sphinx_vcs_changelog.constants import OPTION_FORMAT
from sphinx_vcs_changelog.constants import OPTION_FORMAT_LIST
from sphinx_vcs_changelog.constants import OPTION_FORMAT_TABLE
from sphinx_vcs_changelog.constants import OPTION_ITEM_TEMPLATE
from sphinx_vcs_changelog.constants import OPTION_TABLE_CAPTION
from sphinx_vcs_changelog.constants import OPTION_TABLE_HEADER
from sphinx_vcs_changelog.constants import TABLE_ITEM_PREFIX
from sphinx_vcs_changelog.exceptions import UnexpectedParameterValue
from sphinx_vcs_changelog.repository import Repository


class ChangelogWriter(Repository):
    """Base class for simple linear changelog's"""
    known_commit_properties = [
        'summary',
        'message',
        'name_rev',
        'author'
    ]

    def __init__(self, *args, **kwargs):
        super(ChangelogWriter, self).__init__(*args, **kwargs)
        self._item_template = NOTSET
        self._output_template = NOTSET

    @staticmethod
    def get_list_template():
        """Get list-formatted changelog template"""
        return DEFAULT_LIST_TEMPLATE

    @staticmethod
    def get_table_template():
        """Get table-formatted changelog template"""
        return DEFAULT_TABLE_TEMPLATE

    def get_template(self):
        """Prepare changelog template"""
        if self._output_template != NOTSET:
            return self._output_template

        if self.content:
            self._output_template = '\n'.join((
                x
                for x in self.content
            ))
            return self._output_template

        output_format = self.get_format()
        if output_format == OPTION_FORMAT_LIST:
            self._output_template = self.get_list_template()
        elif output_format == OPTION_FORMAT_TABLE:
            self._output_template = self.get_table_template()
        else:
            raise UnexpectedParameterValue(OPTION_FORMAT, output_format)
        return self._output_template

    def get_list_template_context(self):
        """Get additional context variables for list-formatted template"""
        return dict()

    def get_table_template_context(self):
        """Get additional context variables for table-formatted template"""
        table_header = self.option(OPTION_TABLE_HEADER, DEFAULT_TABLE_HEADER)
        table_caption = self.option(OPTION_TABLE_CAPTION, DEFAULT_TABLE_CAPTION)
        context = dict(
            header=table_header,
            name=table_caption
        )
        line_prefix = '\n'+TABLE_ITEM_PREFIX
        return dict(
            table_options=line_prefix.join([
                ':%(option)s: %(value)s' % dict(option=k, value=v)
                for k, v in context.items()
            ])
        )

    def get_template_context(self):
        """Get context for template fill"""
        context = {}
        for context_updater_class in self.context_processors:
            context_updater = context_updater_class(self)

            if not context_updater.required:
                continue

            for x in self.commits:
                context_updater.collect_commit_info(x)

            context.update(context_updater.context)

        context.update(
            commits='\n'.join((
                self.format_commit_message(x) for x in self.commits
            ))
        )
        output_format = self.get_format()
        if output_format == OPTION_FORMAT_LIST:
            context.update(self.get_list_template_context())
        elif output_format == OPTION_FORMAT_TABLE:
            context.update(self.get_table_template_context())
        else:
            raise UnexpectedParameterValue(OPTION_FORMAT, output_format)

        return context

    def get_list_item_template(self):
        """Get list-formatted changelog item template"""
        template = self.option(
            OPTION_ITEM_TEMPLATE,
            DEFAULT_ITEM_TEMPLATE_LIST
        )
        if not template.startswith(LIST_ITEM_PREFIX):
            template = LIST_ITEM_PREFIX + template
        return template

    def get_table_item_template(self):
        """Get table-formatted changelog item template"""
        template = self.option(
            OPTION_ITEM_TEMPLATE,
            DEFAULT_ITEM_TEMPLATE_TABLE
        )
        if not template.startswith(TABLE_ITEM_PREFIX):
            template = TABLE_ITEM_PREFIX + template
        return template

    def get_item_template(self):
        """Get used item template"""
        if self._item_template != NOTSET:
            return self._item_template

        output_format = self.get_format()
        if output_format == OPTION_FORMAT_LIST:
            self._item_template = self.get_list_item_template()
        elif output_format == OPTION_FORMAT_TABLE:
            self._item_template = self.get_table_item_template()
        else:
            raise UnexpectedParameterValue(OPTION_FORMAT, output_format)
        return self._item_template

    def get_format(self):
        """Get output format"""
        return self.option(OPTION_FORMAT, DEFAULT_FORMAT)

    def prepare_rst(self):
        """Make internal ReStructuredText changelog"""
        template = self.get_template()
        self.info("Using template:\n%s" % template)
        context = self.get_template_context()
        return template.format(**context)

    def build_markup(self):
        """Build markup"""
        from docutils.readers import Reader

        internal_rst = self.prepare_rst()
        self.info("Changelog code:\n%s" % internal_rst)
        internal_rst_fh = StringInput(source=internal_rst)
        reader = Reader(parser_name='rst')

        option_parser = OptionParser()
        settings = option_parser.get_default_values()
        settings.update(
            dict(
                tab_width=3,
                pep_references=False,
                rfc_references=False,
                file_insertion_enabled=True
            ),
            option_parser
        )
        document = reader.read(internal_rst_fh, reader.parser, settings)
        return document.children

    @staticmethod
    def get_commit_dict(commit):
        """Return commit as dict to use in string format
        :param commit: Commit instance
        :type commit: Commit

        :rtype: dict
        """
        assert isinstance(commit, Commit)

        if '\n' in commit.message:
            summary, detailed_message = commit.message.split('\n', 1)
        else:
            summary = commit.message
            detailed_message = None

        return dict(
            summary=summary,
            detail=detailed_message,
            message=commit.message,
            name_rev=commit.name_rev,
            author=commit.author,
            datetime=datetime.fromtimestamp(commit.authored_date),
            date=datetime.fromtimestamp(commit.authored_date).date(),
        )

    def format_commit_message(self, commit):
        """Format commit message & detailed representation"""
        template = self.get_item_template()
        format_args = self.get_commit_dict(commit)
        return template.format(**format_args)
