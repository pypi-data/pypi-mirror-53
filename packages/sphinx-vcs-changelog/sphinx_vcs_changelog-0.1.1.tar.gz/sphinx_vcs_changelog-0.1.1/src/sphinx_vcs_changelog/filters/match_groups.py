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

# -*- coding: utf-8 -*-
from sphinx_vcs_changelog.constants import NOTSET
from sphinx_vcs_changelog.constants import NOTSET_STR
from sphinx_vcs_changelog.constants import OPTION_MATCH_GROUPS
from sphinx_vcs_changelog.filters import ContextExtender


class MatchGroups(ContextExtender):
    """Join commits into groups and provide commit group slices"""
    option = OPTION_MATCH_GROUPS
    is_regexp = True

    def collect_named_group_values_set(self, mo):
        """Collect named groups values set"""
        for k, v in mo.groupdict(default=NOTSET).items():
            key = '%s_set' % k
            value = v is not NOTSET and v or NOTSET_STR
            self.context[key] = self.context.get(key, set()).union([v])

    def collect_named_group_values_count(self, mo):
        """Collect named groups values set"""
        for k, v in mo.groupdict(default=NOTSET).items():
            key = '%s_value_%s_count' % (k, v is not NOTSET and v or NOTSET_STR)
            self.context[key] = self.context.get(key, 0) + 1

    def collect_named_groups(self, mo):
        """Collect some additional info about named groups matches"""
        self.collect_named_group_values_set(mo)
        self.collect_named_group_values_count(mo)

    def collect_commit_info(self, commit):
        """Collect information about commit matched pattern"""
        mo = self.regexp.match(commit.message)
        if mo:
            self.context.update(
                **{'matched': self.context.get('matched', 0) + 1}
            )

