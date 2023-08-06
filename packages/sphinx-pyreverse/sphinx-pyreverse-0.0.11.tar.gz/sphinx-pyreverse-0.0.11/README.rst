Sphinx-pyreverse
=================

A simple sphinx extension to generate a UML diagram from python modules.

Install
--------

Install with:::

    pip install -e git+https://github.com/alendit/sphinx-pyreverse.git#egg=sphinx-pyreverse

Usage
------

Add "sphinx_pyreverse" to the extensions list in your conf.py (make sure it is
in the PYTHONPATH).

Call the directive with path to python module as content. The ``:classes:`` and
``:packages:`` flags specify which UML diagrams to show.::

    .. uml:: {{modulename}}
        :classes:
        :packages:
    
Requires pyreverse from pylint.
