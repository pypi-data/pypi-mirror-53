# -*- coding: utf-8 -*-
"""Command-line handler"""
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

from sphinx_vcs_changelog.changelog import ChangelogWriter
from sphinx_vcs_changelog.factory import directive_factory


def get_options_from_config(config_file):
    """Get configuration information from config like setup.cfg or tox.ini"""
    from six.moves.configparser import ConfigParser
    conf = ConfigParser()

    conf.read([config_file])
    if conf.has_section('changelog'):
        return dict(conf.items('changelog'))
    return {}


def main():
    """Startup point for commandline handler"""
    current_dir = path.curdir

    virtual_name = 'changelog.rst'
    virtual_source = path.join(current_dir, virtual_name)

    instance = directive_factory(virtual_source)
    instance.prepare()

    config = get_options_from_config('setup.cfg')
    instance.options.update(config)

    assert isinstance(instance, ChangelogWriter)

    rst = instance.prepare_rst()
    print(rst)
