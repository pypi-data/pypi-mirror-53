# -*- coding: utf-8 -*-
"""Filter commits to added after specified revision"""
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

from git import Commit

from sphinx_vcs_changelog.constants import OPTION_SINCE
from sphinx_vcs_changelog.filters import OptionFilter


class AddedSince(OptionFilter):
    """Filter commits to added after specified revision"""
    option = OPTION_SINCE
    compare = True

    def pass_to_render(self, commit):
        """Pass commits only after requested commit found"""
        assert isinstance(commit, Commit)
        if commit.message == self.value or commit.hexsha == self.value:
            self.compare = False

        return self.compare
