# -*- coding: utf-8 -*-
"""Filter commits to only matched specified regular expression"""
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
from sphinx_vcs_changelog.constants import OPTION_MATCH
from sphinx_vcs_changelog.filters import OptionFilter


class MatchedRegexp(OptionFilter):
    """Match commit messages with regular expression"""
    option = OPTION_MATCH
    is_regexp = True

    def pass_to_render(self, commit):
        """Pass commit to render only if message matched regexp"""
        return self.regexp.match(commit.message) is not None
