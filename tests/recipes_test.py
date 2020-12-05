from click.testing import CliRunner
from honeybee_radiance_recipe.cli import run_recipe
import os
import shutil


def run_daylight_recipe(recipe_name, extension):
    project_folder = './tests/assets/project folder'
    inputs = './tests/assets/inputs.json'
    name = f'{recipe_name}-test'
    sim_folder = os.path.join(project_folder, name)
    if os.path.exists(sim_folder):
        shutil.rmtree(sim_folder)
    runner = CliRunner()
    result = runner.invoke(
        run_recipe,
        [recipe_name, project_folder, '-i', inputs, '--workers', '2',
         '--name', name]
    )
    assert result.exit_code == 0
    results_folder = os.path.join(sim_folder, 'results')
    assert os.path.isfile(os.path.join(results_folder, f'TestRoom_1.{extension}'))
    assert os.path.isfile(os.path.join(results_folder, f'TestRoom_2.{extension}'))


def test_daylight_factor():
    run_daylight_recipe('daylight-factor', 'res')


def test_annual_daylight():
    run_daylight_recipe('annual-daylight', 'ill')
