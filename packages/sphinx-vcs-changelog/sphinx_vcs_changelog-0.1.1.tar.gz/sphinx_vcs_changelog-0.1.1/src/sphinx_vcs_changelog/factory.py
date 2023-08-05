# -*- coding: utf-8 -*-

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
from os import path

from docutils import frontend
from docutils import statemachine
from docutils.frontend import Values
from docutils.utils import new_document

from sphinx_vcs_changelog.constants import DIRECTIVE_CHANGELOG


def directive_factory(src_path):
    """Create directive instance out of docutils/sphinx process.

    Used in testing or command-line process
    """
    from sphinx_vcs_changelog.changelog import ChangelogWriter

    state_machine = statemachine.StateMachine(
        state_classes=[statemachine.StateWS],
        initial_state='StateWS'
    )
    base_dir = path.dirname(src_path)

    _instance = object.__new__(ChangelogWriter)
    _instance.name = DIRECTIVE_CHANGELOG
    _instance.arguments = []
    _instance.options = {}
    _instance.content = ""
    _instance.lineno = 123
    _instance.content_offset = 123
    _instance.block_text = ""
    _instance.state = state_machine.get_state()
    _instance.state_machine = state_machine

    document = new_document(src_path)
    document.settings.update(
        {'env': Values(defaults={'srcdir': base_dir})},
        frontend.OptionParser()
    )
    setattr(_instance.state, 'document', document)
    _instance.prepare()
    return _instance
