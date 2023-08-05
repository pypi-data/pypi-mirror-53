*********************
NifTools Sphinx Theme
*********************

.. image:: https://img.shields.io/pypi/v/niftools_sphinx_theme.svg
   :target: https://pypi.python.org/pypi/niftools_sphinx_theme
   :alt: PyPi Version
.. image:: https://img.shields.io/travis/com/TagnumElite/niftools_sphinx_theme/develop
   :target: https://travis-ci.com/TagnumElite/niftools_sphinx_theme
   :alt: Build Status
.. image:: https://img.shields.io/pypi/l/niftools_sphinx_theme.svg
   :target: https://pypi.python.org/pypi/niftools_sphinx_theme/
   :alt: License
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code Style: Black

NifTools_ Sphinx_ theme was created to mimic the NifTools_ website,
which is running a `modified version <https://github.com/niftools/niftools.github.io>`_ of Yummy-Jekyl_.

This theme is still in planning/development stage!
Please wait until ver `1.0.0` before using this theme!


Features
========

Supports these extensions:

- ABlog_
- autodoc_
- autosectionlabel_
- autosummary_
- coverage_
- doctest_
- extlinks_
- graphviz_
- ifconfig_
- imgconvertor_
- inhertance_diagram_
- intersphinx_
- linkcode_
- imgmath_ / mathjax_
- napoleon_
- todo_
- viewcode_

Templates
^^^^^^^^^

`See More <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_additional_pages>`_

- About Page
- Blog Page
- Projects Page

Installation
============

This theme can be found on PyPi_ and can be installed through pip

.. code:: console

    pip install --upgrade niftools_sphinx_theme

Inside your sphinx ``conf.py`` file you must put this inside

.. code:: python

    import niftools_sphinx_theme

    extensions = [
        "niftools_sphinx_theme",
        ...
    ]

    html_theme = "niftools_sphinx_theme"

Customization
=============

This theme was created with customization is mind.

Development
===========

I include the built files so all you have to do is run sphinx,
but if you wish to work on this project we use webpack_ to compile
and copy all CSS_, JavaScript_ and fonts to the static folder.

Please read the `contribution guide`_ to understand what to do!

.. _PyPi: https://pypi.python.org/pypi/niftools_sphinx_theme
.. _ABlog: https://ablog.readthedocs.io/
.. _autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _autosectionlabel: https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
.. _autosummary: https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
.. _coverage: https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html
.. _doctest: https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html
.. _extlinks: https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html
.. _graphviz: https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html
.. _ifconfig: https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html
.. _imgconvertor: https://www.sphinx-doc.org/en/master/usage/extensions/imgconverter.html
.. _imgmath: https://www.sphinx-doc.org/en/master/usage/extensions/math.html#module-sphinx.ext.imgmath
.. _inhertance_diagram: https://www.sphinx-doc.org/en/master/usage/extensions/inheritance.html
.. _intersphinx: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
.. _linkcode: https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html
.. _mathjax: https://www.sphinx-doc.org/en/master/usage/extensions/math.html#module-sphinx.ext.mathjax
.. _napoleon: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
.. _todo: https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
.. _viewcode: https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
.. _Sphinx: http://www.sphinx-doc.org
.. _NifTools: https://niftools.org
.. _Yummy-Jekyl: https://github.com/DONGChuan/Yummy-Jekyll/
.. _CSS: https://developer.mozilla.org/en-US/docs/Web/CSS
.. _JavaScript: https://developer.mozilla.org/en-US/docs/Web/JavaScript
.. _webpack: https://webpack.js.org/


.. _contribution guide: