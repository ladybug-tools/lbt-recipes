"""Test Recipe class."""
import os

from honeybee.model import Model
from honeybee.room import Room
from honeybee.config import folders as hb_folders

from lbt_recipes.recipe import Recipe


def test_recipe_init():
    # create a model for simulation
    room = Room.from_box('TinyHouseZone', 5, 10, 3)
    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    model = Model('TinyHouse', [room])
    model.properties.radiance.sensor_grids = \
        [room.properties.radiance.generate_sensor_grid(1, offset=0.8)]

    # pass the model to the recipe
    recipe = Recipe('daylight_factor')
    recipe.input_value_by_name('model', model)
    recipe.input_value_by_name('radiance-parameters', None)

    # set the default project folder based on the model name if available
    recipe.default_project_folder = \
        os.path.join(hb_folders.default_simulation_folder, model.identifier)

    # test the inputs json
    input_json = recipe.write_inputs_json()
    assert os.path.isfile(input_json)

    # check that the inputs have been handled
    for inp in recipe.inputs:
        if inp.name == 'model':
            assert isinstance(inp.value, str)
        if inp.name == 'radiance-parameters':
            assert isinstance(inp.value, str)


def test_recipe_run():
    # create a model for simulation
    room = Room.from_box('TinyHouseZone', 5, 10, 3)
    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    model = Model('TinyHouse', [room])
    model.properties.radiance.sensor_grids = \
        [room.properties.radiance.generate_sensor_grid(1, offset=0.8)]

    # pass the model to the recipe
    recipe = Recipe('daylight_factor')
    recipe.input_value_by_name('model', model)
    recipe.input_value_by_name('radiance-parameters', None)

    # run the recipe
    recipe.run()
