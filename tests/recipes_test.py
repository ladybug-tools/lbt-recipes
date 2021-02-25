from click.testing import CliRunner
import os
import shutil

from ladybug.futil import nukedir
from honeybee_radiance.config import folders as rad_folders
from queenbee_local.cli import run_recipe

# radiance environment variables so that everyone can run locally
genv = {}
genv['PATH'] = rad_folders.radbin_path
genv['RAYPATH'] = rad_folders.radlib_path
env_args = []
for k, v in genv.items():
    env_args.append('--env')
    env_args.append('{}="{}"'.format(k, v))


def run_daylight_recipe(recipe_name, extension):
    project_folder = './tests/assets/project folder'
    recipe_folder = './lbt_recipes/{}'.format(recipe_name.replace('-', '_'))
    inputs = './tests/assets/radiance_grid_inputs.json'
    name = f'{recipe_name}-test'
    sim_folder = os.path.join(project_folder, name)
    if os.path.exists(sim_folder):
        shutil.rmtree(sim_folder)
    runner = CliRunner()
    result = runner.invoke(
        run_recipe,
        [recipe_folder, project_folder, '-i', inputs, '--workers', '2',
         '--name', name, ] + env_args
    )
    assert result.exit_code == 0
    results_folder = os.path.join(sim_folder, 'results')
    assert os.path.isfile(os.path.join(results_folder, f'TestRoom_1.{extension}'))
    assert os.path.isfile(os.path.join(results_folder, f'TestRoom_2.{extension}'))
    nukedir(sim_folder, True)


def test_daylight_factor():
    run_daylight_recipe('daylight-factor', 'res')


def test_annual_daylight():
    run_daylight_recipe('annual-daylight', 'ill')


def run_comfort_map_recipe(recipe_name):
    project_folder = './tests/assets/project folder'
    recipe_folder = './lbt_recipes/{}'.format(recipe_name.replace('-', '_'))
    inputs = './tests/assets/comfort_map_inputs.json'
    name = f'{recipe_name}-test'
    sim_folder = os.path.join(project_folder, name)
    if os.path.exists(sim_folder):
        shutil.rmtree(sim_folder)
    runner = CliRunner()
    result = runner.invoke(
        run_recipe,
        [recipe_folder, project_folder, '-i', inputs, '--workers', '2',
         '--name', name, ] + env_args
    )
    assert result.exit_code == 0
    results_folder = os.path.join(sim_folder, 'results')
    temperature_folder = os.path.join(results_folder, 'temperature')
    assert os.path.isdir(temperature_folder)
    assert os.path.isfile(os.path.join(temperature_folder, 'TestRoom_1.csv'))
    assert os.path.isfile(os.path.join(temperature_folder, 'TestRoom_2.csv'))
    nukedir(sim_folder, True)


def test_adaptive_comfort_map():
    run_comfort_map_recipe('adaptive-comfort-map')


def test_pmv_comfort_map():
    run_comfort_map_recipe('pmv-comfort-map')


def test_utci_comfort_map():
    run_comfort_map_recipe('utci-comfort-map')
