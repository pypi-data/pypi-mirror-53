# -*- coding: utf-8 -*-
"""Define limiter to expected results count as commits filter"""
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


from sphinx_vcs_changelog.constants import OPTION_MAX_RESULTS_COUNT
from sphinx_vcs_changelog.filters import OptionFilter


class ResultsCount(OptionFilter):
    """Filter commits to return no more requested results count"""
    option = OPTION_MAX_RESULTS_COUNT
    compare = 0

    def pass_to_render(self, commit):
        """Count commits and return only first N"""
        self.compare += 1
        return self.compare <= self.value
