"""
Note: This file is auto-generated from a Queenbee recipe and should not be edited or
modified directly. Modify the original recipe instead and re-generate the files.
"""

import luigi
import os
from honeybee_radiance_recipe.recipe_helper import QueenbeeTask, load_input_param


_default_inputs = {
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.'
}


class DaylightFactorSimulationLoop(QueenbeeTask):
    """Run ray-tracing and post-process the results and divide them by sky illuminance."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    fixed_radiance_parameters = luigi.Parameter(default='-I -h')

    sky_illum = luigi.Parameter(default='100000')

    @property
    def grid(self):
        value = os.path.join(self.input()['SplitGrid']['output_grids_folder'].path, self.item['path']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def scene_file(self):
        value = self._input_params['octree_file'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'results').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --sky-illum {sky_illum} --output grid.res'.format(radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, sky_illum=self.sky_illum)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'grid', 'to': 'grid.pts', 'from': self.grid},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'grid.res',
                'to': os.path.join(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name']))
            }]


class DaylightFactorSimulation(luigi.Task):
    """Run ray-tracing and post-process the results and divide them by sky illuminance."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grid_list(self):
        value = self.input()['SplitGrid']['grid_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return load_input_param(self.grid_list)
        except:
            # it is a parameter
            return self.input()['SplitGrid']['grid_list'].path

    def run(self):
        yield [DaylightFactorSimulationLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'daylight_factor_simulation.done'), 'w') as out_file:
            out_file.write('done!\n')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'daylight_factor_simulation.done'))
        }


class SplitGrid(QueenbeeTask):
    """Split a single grid into multiple grids based on maximum number of sensors."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def grid(self):
        value = self._input_params['sensor_grid'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance grid split grid.pts {sensor_count} --folder output --log-file output/grids.json'.format(sensor_count=self.sensor_count)

    def output(self):
        return {

            'output_grids_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'sub_grids')
            ),
            'grid_list': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'output/grids.json')
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'grid', 'to': 'grid.pts', 'from': self.grid}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-grids-folder', 'from': 'output',
                'to': os.path.join(self.execution_folder, 'sub_grids')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'grid-list', 'from': 'output/grids.json', 'to': os.path.join(self.params_folder, 'output/grids.json')}]


class _RayTracingOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [DaylightFactorSimulation(_input_params=self.input_values)]
