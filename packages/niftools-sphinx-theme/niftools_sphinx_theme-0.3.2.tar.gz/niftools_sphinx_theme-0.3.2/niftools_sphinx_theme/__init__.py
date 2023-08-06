"""
NifTools Sphinx Theme, created to mimic the niftools.org website
"""
from os import path
import logging

# noinspection PyUnreachableCode
if False:  # Required for typing, not for code
    import sphinx.application

__version__ = "0.3.2"


def get_theme_path():
    """Return list of HTML theme paths."""
    return path.abspath(path.dirname(path.dirname(__file__)))


def get_templates_path():
    return path.join(get_theme_path(), "templates")


def _clean_fonts(val):  # type: (str) -> str
    return "|".join([x.strip().replace(" ", "+") for x in val.split(",")])


def build_initialized(app):  # type: (sphinx.application.Sphinx) -> None
    app.builder.templates.environment.filters["niftools_clean_fonts"] = _clean_fonts


def setup(app):  # type: (sphinx.application.Sphinx) -> dict
    app.add_html_theme("niftools_sphinx_theme", path.abspath(path.dirname(__file__)))
    app.connect("builder-inited", build_initialized)
    return {"version": __version__}
