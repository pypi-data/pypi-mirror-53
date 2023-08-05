# -*- coding: utf-8 -*-
"""Base"""
from abc import abstractmethod
from future import standard_library
from sphinx_vcs_changelog.constants import OPTION_FORMAT
from sphinx_vcs_changelog.constants import OPTION_TABLE_CAPTION
from sphinx_vcs_changelog.constants import OPTION_TABLE_HEADER

standard_library.install_aliases()
from itertools import filterfalse
from os import path

import six
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from git import InvalidGitRepositoryError
from git import NoSuchPathError
from git import Repo

from sphinx_vcs_changelog.constants import OPTION_ITEM_TEMPLATE
from sphinx_vcs_changelog.constants import OPTION_MATCH
from sphinx_vcs_changelog.constants import OPTION_MATCH_GROUPS
from sphinx_vcs_changelog.constants import OPTION_MAX_RESULTS_COUNT
from sphinx_vcs_changelog.constants import OPTION_REPO_DIR
from sphinx_vcs_changelog.constants import OPTION_SINCE
from sphinx_vcs_changelog.exceptions import InvalidPath
from sphinx_vcs_changelog.exceptions import NoCommits
from sphinx_vcs_changelog.exceptions import RepositoryNotFound
from sphinx_vcs_changelog.filters import CommitsFilter
from sphinx_vcs_changelog.filters import NOTSET
from sphinx_vcs_changelog.filters.added_since import AddedSince
from sphinx_vcs_changelog.filters.match_groups import MatchGroups
from sphinx_vcs_changelog.filters.matched_regexp import MatchedRegexp
from sphinx_vcs_changelog.filters.results_count import ResultsCount


class Repository(Directive):
    """Base class for changelog directive

    Provides access method to VCS repository definition,
    commits filtering and options definitions
    """

    filters = [
        AddedSince,
        MatchedRegexp,
        ResultsCount
    ]
    context_processors = [
        MatchGroups
    ]
    has_content = True

    option_spec = {
        OPTION_REPO_DIR: six.text_type,
        OPTION_SINCE: six.text_type,
        OPTION_MATCH: six.text_type,
        OPTION_MAX_RESULTS_COUNT: directives.nonnegative_int,
        OPTION_MATCH_GROUPS: six.text_type,
        OPTION_ITEM_TEMPLATE: six.text_type,
        OPTION_FORMAT: six.text_type,
        OPTION_TABLE_HEADER: six.text_type,
        OPTION_TABLE_CAPTION: six.text_type
    }

    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)
        self.debug = None
        self.info = None
        self.warning = None
        self.error = None
        self.critical = None
        self._filtered = None

        self.prepare()

    def prepare(self):
        """Separated initialisation.
        Called from __init__ during work process
        as well as directly in tests.

        Dont inline into __init__ because of testing behaviour"""
        from sphinx.util import logging
        logger = logging.getLogger(__name__)

        self.debug = logger.debug
        self.info = logger.info
        self.warning = logger.warning
        self.error = logger.debug
        self.critical = logger.error

        self._filtered = None

    def using_repo(self):
        """Find target repository and return Repo object.

        :returns: Repo
        """
        repo_dir = self.options.get(
            OPTION_REPO_DIR,
            self.state.document.settings.env.srcdir
        )
        if not path.exists(repo_dir):
            raise InvalidPath("No such path %s" % repo_dir)

        try:
            repo = Repo(repo_dir, search_parent_directories=True)

        except InvalidGitRepositoryError:
            raise RepositoryNotFound("No repository at %s", repo_dir)

        except NoSuchPathError:
            raise InvalidPath("No such path %s" % repo_dir)

        return repo

    @property
    def repo(self):
        """Get current repository as property"""
        return self.using_repo()

    def option(self, option_name, default=None):
        """Shorthand method to get options"""
        if option_name not in self.option_spec:
            raise NotImplementedError("No such option %s" % option_name)
        return self.options.get(option_name, default)

    def option_configured(self, option_name):
        """Check if option is set to any value"""
        return not self.options.get(option_name, NOTSET) == NOTSET

    @property
    def commits(self):
        """Iterator over repository commits.

        Filtering commits using current filter set"""
        if self._filtered is None:
            try:
                self._filtered = self.using_repo().iter_commits()
            except ValueError:
                raise NoCommits()

        for filter_instance_or_class in self.get_filter_ordering():
            self._apply_filter(filter_instance_or_class)

        return self._filtered

    @property
    def commits_messages(self):
        """Iterator over repository commits messages"""
        self._filtered = None
        for x in self.commits:
            yield x.message

    @property
    def commits_list(self):
        """List of repository commits to render"""
        self._filtered = None
        return list(self.commits)

    @property
    def commits_count(self):
        """Count filtered commits count"""
        return len(self.commits_list)

    def _apply_filter(self, filter_class):
        """Apply additional filter to commits iterator"""
        _instance = self.get_filter_instance(filter_class)
        if not _instance.required:
            return

        self._filtered = filterfalse(_instance.filter_function, self._filtered)

    def get_filter_instance(self, filter_class):
        """Make filter instance by filter_class"""
        assert issubclass(filter_class, CommitsFilter)
        return filter_class(self)

    def get_filter_ordering(self):
        """Return filter functions apply ordering"""
        return self.filters

    def run(self):
        """Choose commits to display & build markup """
        return self.build_markup()

    @abstractmethod
    def build_markup(self):
        """Build markup"""
        raise NotImplementedError("%s.build_markup() to be implemented")
