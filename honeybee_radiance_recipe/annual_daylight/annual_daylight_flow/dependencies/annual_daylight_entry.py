"""
Note: This file is auto-generated from a Queenbee recipe and should not be edited or
modified directly. Modify the original recipe instead and re-generate the files.
"""

import luigi
import os
from honeybee_radiance_recipe.recipe_helper import QueenbeeTask, load_input_param


_default_inputs = {   'octree_file': None,
    'octree_file_with_suns': None,
    'params_folder': '__params',
    'radiance_parameters': ' ',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None,
    'sky_matrix_direct': None,
    'sun_modifiers': None}


class DirectSkyLoop(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -ab 1 -c 1 -fad'

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def sky_matrix(self):
        value = self._input_params['sky_matrix_direct'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sky_dome(self):
        value = self._input_params['sky_dome'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
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
        return os.path.join(self._input_params['simulation_folder'], 'direct_sky').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}"'.format(sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'results.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class DirectSky(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
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
        yield [DirectSkyLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'direct_sky.done'), 'w') as out_file:
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
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'direct_sky.done'))
        }


class DirectSunlightLoop(QueenbeeTask):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers using
rcontrib command."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -fad -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0'

    @property
    def sensor_count(self):
        return self.item['count']

    calculate_values = luigi.Parameter(default='value')

    @property
    def modifiers(self):
        value = self._input_params['sun_modifiers'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['SplitGrid']['output_grids_folder'].path, self.item['path']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def scene_file(self):
        value = self._input_params['octree_file_with_suns'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'direct_sunlight').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance dc scontrib scene.oct grid.pts suns.mod --{calculate_values} --sensor-count {sensor_count} --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --output results.ill'.format(calculate_values=self.calculate_values, sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifiers', 'to': 'suns.mod', 'from': self.modifiers},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'results.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class DirectSunlight(luigi.Task):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers using
rcontrib command."""
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
        yield [DirectSunlightLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'direct_sunlight.done'), 'w') as out_file:
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
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'direct_sunlight.done'))
        }


class OutputMatrixMathLoop(QueenbeeTask):
    """Remove direct sky from total sky and add direct sun."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    conversion = luigi.Parameter(default='47.4 119.9 11.6')

    output_format = luigi.Parameter(default='-fa')

    @property
    def direct_sky_matrix(self):
        value = 'direct_sky/{item_name}.ill'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def total_sky_matrix(self):
        value = 'total_sky/{item_name}.ill'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sunlight_matrix(self):
        value = 'direct_sunlight/{item_name}.ill'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'final').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'rmtxop {output_format} sky.ill + -s -1.0 sky_dir.ill + sun.ill -c {conversion} | getinfo - > final.ill'.format(output_format=self.output_format, conversion=self.conversion)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params), 'DirectSunlight': DirectSunlight(_input_params=self._input_params), 'TotalSky': TotalSky(_input_params=self._input_params), 'DirectSky': DirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'direct_sky_matrix', 'to': 'sky_dir.ill', 'from': self.direct_sky_matrix},
            {'name': 'total_sky_matrix', 'to': 'sky.ill', 'from': self.total_sky_matrix},
            {'name': 'sunlight_matrix', 'to': 'sun.ill', 'from': self.sunlight_matrix}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'final.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class OutputMatrixMath(luigi.Task):
    """Remove direct sky from total sky and add direct sun."""
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
        yield [OutputMatrixMathLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'output_matrix_math.done'), 'w') as out_file:
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
        return {'SplitGrid': SplitGrid(_input_params=self._input_params), 'DirectSunlight': DirectSunlight(_input_params=self._input_params), 'TotalSky': TotalSky(_input_params=self._input_params), 'DirectSky': DirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'output_matrix_math.done'))
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


class TotalSkyLoop(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1 -fad'

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def sky_matrix(self):
        value = self._input_params['sky_matrix'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sky_dome(self):
        value = self._input_params['sky_dome'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
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
        return os.path.join(self._input_params['simulation_folder'], 'total_sky').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}"'.format(sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'results.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class TotalSky(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
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
        yield [TotalSkyLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'total_sky.done'), 'w') as out_file:
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
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'total_sky.done'))
        }


class _AnnualDaylightEntryOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [OutputMatrixMath(_input_params=self.input_values)]
