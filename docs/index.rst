Welcome to lbt-recipes' documentation!
=======================================

A collection of recipes that ship with the Ladybug Tools plugins.

This includes Radiance recipes, which automate the process of running daylight and radiation studies using `Radiance <https://radiance-online.org/>`_.

It also includes microclimate mapping recipes, which spatially map thermal comfort using `EnergyPlus <https://github.com/NREL/EnergyPlus/>`_ and `Radiance <https://radiance-online.org/>`_.

Installation
============

```console
pip install lbt-recipes
```

Local Development
=================

1) Clone this repo locally


   ``git clone git@github.com:ladybug-tools/lbt-recipes``

   # or

   ``git clone https://github.com/ladybug-tools/lbt-recipes``


2) Install dependencies::

      cd lbt-recipes
      pip install -r dev-requirements.txt
      pip install -r requirements.txt


3) Run Tests:

   ``python -m pytest ./tests``


lbt_recipes
=============

.. toctree::
  :maxdepth: 2

  modules

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
