#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Настройки сборки документации для проекта"""
import datetime
import os
import sys

# Get configuration information from setup.cfg
from six.moves.configparser import ConfigParser
conf = ConfigParser()

conf.read([os.path.join(os.path.dirname(__file__), '..', 'setup.cfg')])
setup_cfg = dict(conf.items('metadata'))

project = setup_cfg['project']
package = setup_cfg['package']
author = setup_cfg['author']
copyright = f"{datetime.datetime.now().year}, {setup_cfg['author']}"

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__, )), 'src')))

extensions = [
    'sphinx_vcs_changelog'
]

# Расширение файлов по умолчанию
source_suffix = ['.rst']

# Основной документ
master_doc = 'index'

# Основной язык документа
language = setup_cfg.get('language', 'en')

# Исключить пути и файлы из сборки
exclude_patterns = []

numfig = True
numfig_secnum_depth = 2


# Стиль расцветки блоков кода
# pygments_style = 'sphinx'
pygments_style = 'friendly'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Добавить дополнительные статические файлы из папки _static
html_static_path = ['_static']
# .. и включить их использование в шаблоне
html_context = {
    'css_files': [
        '_static/tables.css'
    ],
}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

html_baseurl = '/'
html_copy_source = False
html_show_sourcelink = False
html_link_suffix = '.html'
html_show_sphinx = False
html_search_language = 'ru'
html_show_copyright = False

today_fmt = '%x'

# modindex_common_prefix = [f'{package}']

#
# Настройки сборки PDF
# Использовать пакет xelatex для сборки
latex_engine = 'xelatex'
# Формат листа по умолчанию
latex_paper_size = 'a4'
# Показывать гиперссылки в подвале страницы
latex_show_urls = 'footnotes'
# Использовать многоязычный индекс
latex_use_xindy = True
# Добавлять специфичные индексы
latex_domain_indices = True
# Добавлять номера страниц в ссылки
# latex_show_pagerefs = True
latex_preamble = r"""
\setlength{\tymin}{40pt} % минимальная ширина стобца в таблице
"""

latex_elements = {
    'preamble': latex_preamble,
    'pointsize': '10pt',
    # disallow fancy chapter titles, only useful without oneside
    'fncychap': '',
    # openany: allow chapters to start on any page
    # oneside: one-side document
    'extraclassoptions': 'openany,oneside',
    'sphinxsetup': 'hmargin={1in,1in}, vmargin={1in,1in}, marginpar=0.1in',
    # 'fontenc': '\\usepackage[T1,T2A]{fontenc}',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [(
    'index', setup_cfg['package'] + '.tex', project, author, 'manual', False
)]
