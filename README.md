[![Build Status](https://github.com/ladybug-tools/honeybee-radiance-recipe/workflows/CI/badge.svg)](https://github.com/ladybug-tools/honeybee-radiance-recipe/actions)

# honeybee-radiance-recipe

Collection of recipes for running daylight studies using honeybee-radiance.

Honeybee Radiance recipe library is a collection of recipes to automate the process of running lighting studies using [Radiance](http://radiance-online.org/).

`honeybee-radiance-recipe` is built on top of [`honeybee-radiance`](https://github.com/ladybug-tools/honeybee-radiance). It uses [`radiance-folder-structure`](https://github.com/ladybug-tools/radiance-folder-structure) as the input for running recipes. As long as you follow the folder structure you should be able to use these recipes regardless of how the folder is generated. :rocket:

## Installation

```console
pip install honeybee-radiance-recipe
```

## Local Development

1. Clone this repo locally

```console
git clone git@github.com:ladybug-tools/honeybee-radiance-recipe

# or

git clone https://github.com/ladybug-tools/honeybee-radiance-recipe
```

2. Install dependencies:

```console
cd honeybee-radiance-recipe
pip install -r dev-requirements.txt
```
