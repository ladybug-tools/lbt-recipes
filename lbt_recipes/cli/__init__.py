"""Command Line Interface (CLI) entry point for lbt-recipes."""
import click
import sys
import logging
import json

from lbt_recipes.recipe import Recipe
from lbt_recipes.settings import RecipeSettings

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    pass


@main.command('run')
@click.argument('recipe-name', type=str)
@click.argument(
    'inputs',
    type=click.Path(exists=True, file_okay=True, resolve_path=True, dir_okay=False)
)
@click.option(
    '-p', '--project-folder',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, dir_okay=True),
    default=None, help='Path to a project folder in which the recipe will be '
    'executed. If None, the default project folder for the Recipe will be used.'
)
@click.option(
    '-w', '--workers', type=int, default=2, show_default=True,
    help='An integer to set the number of CPUs used in the execution of the '
    'recipe. This number should not exceed the number of CPUs on the '
    'machine running the simulation and should be lower if other tasks '
    'are running while the simulation is running.'
)
@click.option(
    '-d', '--debug', default=None,
    type=click.Path(exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    help='Optional path to a debug folder. If debug folder is provided all the steps '
    'of the simulation will be executed inside the debug folder which can be used for '
    'furthur inspection.'
)
def run(recipe_name, inputs, project_folder, workers, debug):
    """Run a recipe that is installed within the lbt-recipes package.

    \b
    Args:
        recipe_name: The name of a recipe within the package to be
            executed (eg. pmv-comfort-map).
        inputs: Path to the JSON file that specifies inputs for the recipe.
    """
    try:
        # create the recipe object and assign all of the inputs from the JSON
        recipe = Recipe(recipe_name)
        with open(inputs) as inf:
            data = json.load(inf)
        for inp_name, inp_val in data.items():
            recipe.input_value_by_name(inp_name, inp_val)

        # create the run settings from the other inputs
        settings = RecipeSettings(workers=workers)
        if project_folder is not None:
            settings.folder = project_folder

        # run the recipe
        recipe.run(settings, queenbee_path='queenbee', debug_folder=debug)
    except Exception as e:
        _logger.exception('Failed to execute {} recipe.\n{}'.format(recipe_name, e))
        sys.exit(1)
    else:
        sys.exit(0)


@main.command('viz')
def viz():
    """Check if lbt-recipes is flying!"""
    click.echo('viiiiiiiiiiiiizzzzzzzzz!')


if __name__ == "__main__":
    main()
