# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Geomosaic'
copyright = '2024, Giovannelli Lab.'
author = 'Davide Corso'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    "myst_parser",
]

source_suffix = [".rst", ".md"]
myst_enable_extensions = ["colon_fence", "dollarmath", "amsmath"]
myst_heading_anchors = 5

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_logo = "_static/images/geomosaic_logo_multicolor_300dpi.png"
html_title = ""
html_favicon = "_static/images/favicon.png"
html_static_path = ['_static']
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "admonition-font-size": "100%",
        "admonition-title-font-size": "92%"
    }
}
html_css_files = ["css/custom.css"]
