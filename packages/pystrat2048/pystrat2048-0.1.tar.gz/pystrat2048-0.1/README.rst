
.. image:: https://circleci.com/gh/sdpython/pystrat2048/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/pystrat2048/tree/master

pystrat2048
===========

.. image:: https://raw.githubusercontent.com/sdpython/pystrat2048/master/doc/_static/logo.png
    :width: 50

Simple template to package a strategy for the 2048 game. Material for teaching
`ensae_teaching_cs <https://github.com/sdpython/ensae_teaching_cs>`_.
It implements basic CI and documentation. One example of use:
`strat2048.py
<https://github.com/sdpython/pystrat2048/blob/master/examples/strat2048.py>`_.

Generate the setup in subfolder ``dist``:

::

    python setup.py sdist

Generate the documentation in folder ``dist/html``:

::

    python -m sphinx -T -b html doc dist/html

Run the unit tests:

::

    python -m unittest discover tests

Or:

::

    python -m pytest
    
To check style:

::

    python -m flake8 pystrat2048 tests examples
