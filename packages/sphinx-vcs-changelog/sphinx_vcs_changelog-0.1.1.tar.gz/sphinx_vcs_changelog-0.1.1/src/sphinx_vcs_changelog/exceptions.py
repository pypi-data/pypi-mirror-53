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


class ParamMissed(Exception):
    """Required param missed"""

    def __init__(self, param_name, msg, **kwargs):
        self.param_name = param_name
        if kwargs:
            msg %= kwargs
        self.message = msg
        super(ParamMissed, self).__init__()

    def __str__(self):
        return "%(base_description)s: Expected %(param_name)s. %(msg)s" % dict(
            base_description=self.__class__.__doc__,
            param_name=self.param_name,
            msg=self.message
        )


class RepositoryNotFound(Exception):
    """Repository not found in path"""
    pass


class InvalidPath(Exception):
    """No such path"""
    pass


class NoCommits(Exception):
    """No commits in vcs"""
    pass


class UnexpectedParameterValue(Exception):
    """Parameter value unexpected"""

    def __init__(self, param_name, value, msg, **kwargs):
        self.param_name = param_name
        self.value = value
        if kwargs:
            msg %= kwargs
        self.message = msg
        super(UnexpectedParameterValue, self).__init__()

    def __str__(self):
        return ""\
            "%(base_description)s: " \
            "Parameter %(param_name)s=%(value)s unexpected. " \
            "%(msg)s" % dict(
                base_description=self.__class__.__doc__,
                param_name=self.param_name,
                value=self.vsalue,
                msg=self.message
            )
