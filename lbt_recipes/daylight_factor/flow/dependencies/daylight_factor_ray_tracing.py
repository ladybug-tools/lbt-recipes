"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
from queenbee_local import QueenbeeTask


_default_inputs = {   'grid_name': None,
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -aa 0.1 -ad 2048 -ar 64',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.'}


class MergeResults(QueenbeeTask):
    """Merge several files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return '.res'

    @property
    def folder(self):
        value = 'results'.replace('\\', '/')
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
        return 'honeybee-radiance grid merge input_folder grid {extension} --name {name}'.format(extension=self.extension, name=self.name)

    def requires(self):
        return {'RayTracing': RayTracing(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '../../results/{name}.res'.format(name=self.name))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'input_folder', 'from': self.folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': '{name}{extension}'.format(name=self.name, extension=self.extension),
                'to': os.path.join(self.execution_folder, '../../results/{name}.res'.format(name=self.name))
            }]


class RayTracingLoop(QueenbeeTask):
    """Run ray-tracing and post-process the results for a daylight factor simulation."""

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
        value = os.path.join(self.input()['SplitGrid']['output_folder'].path, self.item['path']).replace('\\', '/')
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
            'result': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'grid', 'to': 'grid.pts', 'from': self.grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result', 'from': 'grid.res',
                'to': os.path.join(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name']))
            }]


class RayTracing(luigi.Task):
    """Run ray-tracing and post-process the results for a daylight factor simulation."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = self.input()['SplitGrid']['grids_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return self.input()['SplitGrid']['grids_list'].path

    def run(self):
        yield [RayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'ray_tracing.done'), 'w') as out_file:
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
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'ray_tracing.done'))
        }


class SplitGrid(QueenbeeTask):
    """Split a single sensor grid file into multiple smaller grids."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def input_grid(self):
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
        return 'honeybee-radiance grid split grid.pts {sensor_count} --folder output --log-file output/grids_info.json'.format(sensor_count=self.sensor_count)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'sub_grids')
            ),
            'grids_list': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'output/grids_info.json')
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_grid', 'to': 'grid.pts', 'from': self.input_grid, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output',
                'to': os.path.join(self.execution_folder, 'sub_grids')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'grids-list', 'from': 'output/grids_info.json', 'to': os.path.join(self.params_folder, 'output/grids_info.json')}]


class _DaylightFactorRayTracing_5c235853Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [MergeResults(_input_params=self.input_values)]
