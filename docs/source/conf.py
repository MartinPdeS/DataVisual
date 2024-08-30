#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from MPSPlots.styles import use_mpsplots_style
import DataVisual
from DataVisual.tools.directories import project_path, doc_css_path

sys.path.insert(0, project_path)
sys.path.insert(0, project_path.joinpath('DataVisual'))


def setup(app):
    app.add_css_file(str(doc_css_path))


autodoc_mock_imports = [
    'numpy',
    'matplotlib',
]

project = 'DataVisual'
copyright = '2024, Martin Poinsinet de Sivry-Houle'
author = 'Martin Poinsinet de Sivry-Houle'
today_fmt = '%B %d, %Y'

version = DataVisual.__version__


extensions = [
    'sphinx.ext.mathjax',
    'numpydoc',
    'pyvista.ext.plot_directive',
    'sphinx_gallery.gen_gallery',
]


def reset_mpl(gallery_conf, fname):
    use_mpsplots_style()


try:
    import pyvista
    if sys.platform in ["linux", "linux2"]:
        pyvista.start_xvfb()  # Works only on linux system!
except ImportError:
    print('Could not load pyvista library for 3D rendering')

sphinx_gallery_conf = {
    "examples_dirs": [],
    "gallery_dirs": [],
    'image_scrapers': ('matplotlib'),
    'ignore_pattern': '/__',
    'plot_gallery': True,
    'reset_modules': reset_mpl,
    'thumbnail_size': [600, 600],
    'download_all_examples': False,
    'line_numbers': False,
    'remove_config_comments': True,
    'capture_repr': ('_repr_html_', '__repr__'),
    'nested_sections': True,
}

autodoc_default_options = {
    'members': False,
    'members-order': 'bysource',
    'undoc-members': False,
    'show-inheritance': True,
    'ignore-module-all': True
}

numpydoc_show_class_members = False

source_suffix = '.rst'

master_doc = 'index'

language = 'en'

highlight_language = 'python3'

html_theme = "pydata_sphinx_theme"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

exclude_trees = []
default_role = "autolink"
pygments_style = "sphinx"

# -- Sphinx-gallery configuration --------------------------------------------
binder_branch = "main"

major, minor = version[:2]
binder_branch = f"v{major}.{minor}.x"

html_theme_options = {
    # Navigation bar
    "logo": {
        "alt_text": "DataVisual's logo",
        "text": "DataVisual",
        "link": "https://datavisual.readthedocs.io/en/latest/",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MartinPdeS/DataVisual",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/datavisual/",
            "icon": "fa-solid fa-box",
        },
    ],
    "navbar_align": "left",
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "show_prev_next": False,
    "show_version_warning_banner": True,
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    # Other
    "pygment_light_style": "default",
    "pygment_dark_style": "github-dark",
}


htmlhelp_basename = 'DataVisualdoc'

latex_elements = {}


latex_documents = [
    (master_doc, 'DataVisual.tex', 'DataVisual Documentation',
     'Martin Poinsinet de Sivry-Houle', 'manual'),
]

man_pages = [
    (master_doc, 'datavisual', 'DataVisual Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'DataVisual', 'DataVisual Documentation',
     author, 'DataVisual', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project

html_static_path = ['_static']
templates_path = ['_templates']
html_css_files = ['default.css']
epub_exclude_files = ['search.html']


# -- MyST --------------------------------------------------------------------
myst_enable_extensions = [
    # Enable fieldlist to allow for Field Lists like in rST (e.g., :orphan:)
    "fieldlist",
]
