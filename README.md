[![Build Status](https://github.com/ladybug-tools/lbt-recipes/workflows/CI/badge.svg)](https://github.com/ladybug-tools/lbt-recipes/actions)

# lbt-recipes

A collection of recipes that ship with the Ladybug Tools plugins.

This includes Radiance recipes, which automate the process of running daylight and radiation studies using [Radiance](http://radiance-online.org/).

It also includes microclimate mapping recipes, which spatially map thermal comfort using [EnergyPlus](https://github.com/NREL/EnergyPlus) and [Radiance](http://radiance-online.org/).

## Installation

`pip install -U lbt-recipes`

To check if command line interface is installed correctly use `lbt-recipes viz` and you
should get a `viiiiiiiiiiiiizzzzzzzzz!` back in response!

## Local Development

1. Clone this repo locally

```console
git clone git@github.com:ladybug-tools/lbt-recipes

# or

git clone https://github.com/ladybug-tools/lbt-recipes
```

2. Install dependencies:

```console
cd lbt-recipes
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:

```console
python -m pytest ./tests
```
