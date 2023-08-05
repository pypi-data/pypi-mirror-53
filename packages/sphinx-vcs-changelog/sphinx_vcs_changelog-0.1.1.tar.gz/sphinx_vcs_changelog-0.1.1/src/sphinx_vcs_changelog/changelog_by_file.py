# # -*- coding: utf-8 -*-
# """Make changelog filtered by file path"""
# TODO: made ChangeLogByPath work
# import re
#
# import six
# from docutils import nodes
#
# from sphinx_vcs_changelog.decorator import use_option
#
#
# @use_option('filename_filter', six.text_type)
# class GitChangelogByFile(LinearChangelog):
#     """Linear changelog"""
#
#     def build_markup(self, commits):
#         """Build markup"""
#         list_node = nodes.bullet_list()
#         for commit in commits:
#             item = self.format_commit_message(commit)
#             list_node.append(item)
#         return [list_node]
#
#     def filter_commits(self, repo):
#         """Get pre-filtered commits by parent class & filter by filename(s) """
#         commits = super(GitChangelogByFile, self).filter_commits(repo)
#         return self.filter_commits_on_filenames(commits)
#
#     def filter_commits_on_filenames(self, commits):
#         """Filter commits to only contained filename(s)"""
#         filtered_commits = []
#         filter_exp = re.compile(self.options.get('filename_filter', r'.*'))
#         for commit in commits:
#             # SHA of an empty tree found at
#             # http://stackoverflow.com/questions/33916648/get-the-diff
#             # -details-of-first-commit-in-gitpython
#             # will be used to get the list of files of initial commit
#             compared_with = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
#             if len(commit.parents) > 0:  # pylint: disable=len-as-condition
#                 compared_with = commit.parents[0].hexsha
#             for diff in commit.diff(compared_with):
#                 if filter_exp.match(diff.a_path) or \
#                         filter_exp.match(diff.b_path):
#                     filtered_commits.append(commit)
#                     break
#
#         return filtered_commits
