"""Honeybee radiance recipes command line interface."""
try:
    import click
except ImportError:
    raise ImportError(
        'click module is not installed. Try `pip install queenbee[cli]` command.'
    )

import json
import os
import time
import pathlib
import sys
import sysconfig
import subprocess

from honeybee.cli import main


# TODO: move this to a honeybee-recipes module so other recipe libraries can also add
# commands to recipe sub-command. This is a proof of concept.
@click.group(help='Commands for interacting with honeybee recipes.')
def recipe():
    pass


@recipe.command('run')
@click.argument('recipe-name', type=click.STRING)
@click.argument(
    'project_folder',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, dir_okay=True),
    default='.'
)
@click.option(
    '-i', '--inputs',
    type=click.Path(exists=True, file_okay=True, resolve_path=True, dir_okay=False),
    default=None, show_default=True, help='Path to the JSON file to'
    ' overwrite inputs for this recipe.'
)
@click.option(
    '-w', '--workers', type=int, default=1, show_default=True,
    help='Number of workers to execute tasks in parallel.'
)
@click.option(
    '-e', '--env', multiple=True, help='An option to pass environmental variables to '
    'commands. Use = to separate key and value. RAYPATH=/usr/local/lib/ray'
)
@click.option('-n', '--name', help='Simulation name for this run.')
@click.option(
    '-d', '--debug',
    type=click.Path(exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    help='Optional path to a debug folder. If debug folder is provided all the steps '
    'of the simulation will be executed inside the debug folder which can be used for '
    'furthur inspection.'
)
def run_recipe(recipe_name, project_folder, inputs, workers, env, name, debug):
    """Run a honeybee recipe.

    \b
    Args:
        recipe_name: Name of a honeybee recipe.
        project_folder: Path to project folder. (Default: '.')
    """
    cli_dir = os.path.dirname(__file__)

    # TODO: Use importlib instead - this is a proof of concept
    recipe_name = recipe_name.replace('-', '_')
    recipe_path = pathlib.Path(cli_dir, f'./{recipe_name}/{recipe_name}.py').as_posix()

    if not os.path.isfile(recipe_path):
        raise ValueError(f'Failed to find {recipe_name} recipe.')

    env_vars = {}
    genv = os.environ.copy()
    if env:
        for e in env:
            try:
                key, value = e.split('=')
            except Exception as e:
                raise ValueError(f'env input is not formatted correctly: {e}')
            else:
                env_vars[key.strip()] = pathlib.Path(value.strip()).as_posix()

        for k, v in env_vars.items():
            k = k.strip()
            if k.upper() == 'PATH':
                # extend the new PATH to current PATH
                genv['PATH'] = os.pathsep.join((v, genv['PATH']))
                continue
            elif k.upper() == 'RAYPATH':
                # extend RAYPATH to current RAYPATH
                try:
                    genv['RAYPATH'] = os.pathsep.join((v, genv['RAYPATH']))
                except KeyError:
                    # it will be set below
                    pass
                else:
                    continue
            # overwrite env variable
            genv[k.strip()] = v.strip()

    if inputs:
        # try to load the results
        with open(inputs) as user_input:
            input_values = json.load(user_input)
    else:
        input_values = {}

    # add simulation folder based on simulation name
    if not name:
        name = f'{recipe_name.replace("-", "_")}_{int(round(time.time(), 2) * 100)}'

    simulation_folder = pathlib.Path(project_folder, name)
    input_values['simulation_folder'] = simulation_folder.as_posix()
    simulation_folder.mkdir(exist_ok=True)

    if debug:
        debug_folder = pathlib.Path(debug)
        if not debug_folder.exists():
            debug_folder.mkdir(0o777)
        input_values['__debug__'] = debug_folder.as_posix()

    # write updated inputs to project folder
    inputs_file = pathlib.Path(
        input_values['simulation_folder'], '__inputs__.json'
    ).as_posix()

    with open(inputs_file, 'w') as inpf:
        json.dump(input_values, inpf)

    python_executable_path = sys.executable

    # add path to scripts folder to env
    scripts_path = sysconfig.get_paths()['scripts']
    genv['PATH'] = os.pathsep.join((scripts_path, genv['PATH']))

    # put all the paths in quotes - this should address the issue for paths with
    # white space
    command = f'"{python_executable_path}" "{recipe_path}" ' \
        f'"{project_folder}" "{inputs_file}" {workers}'

    try:
        subprocess.call(command, cwd=project_folder, shell=True, env=genv)
    except Exception:
        print(f'Failed to execute {recipe_name} recipe...')
        sys.exit(1)
    else:
        sys.exit(0)


main.add_command(recipe)
