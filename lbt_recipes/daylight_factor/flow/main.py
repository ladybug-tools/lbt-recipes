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
from .dependencies.daylight_factor_ray_tracing import _DaylightFactorRayTracing_5c235853Orchestrator as DaylightFactorRayTracing_5c235853Workerbee


_default_inputs = {   'grid_filter': '*',
    'model': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -aa 0.1 -ad 2048 -ar 64',
    'sensor_count': 200,
    'simulation_folder': '.'}


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = self.input()['CreateRadFolder']['model_folder'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sky(self):
        value = self.input()['GenerateSky']['sky'].path.replace('\\', '/')
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
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'GenerateSky': GenerateSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/scene.oct')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': os.path.join(self.execution_folder, 'resources/scene.oct')
            }]


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def input_model(self):
        value = self._input_params['model'].replace('\\', '/')
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
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'model')
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/grids_info.json')
            ),
            'sensor_grids': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'model/grid/_info.json')
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': os.path.join(self.execution_folder, 'model')
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': os.path.join(self.execution_folder, 'results/grids_info.json')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': os.path.join(self.params_folder, 'model/grid/_info.json')}]


class DaylightFactorRayTracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def octree_file(self):
        value = self.input()['CreateOctree']['scene_file'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['CreateRadFolder']['model_folder'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'sensor_count': self.sensor_count,
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DaylightFactorRayTracing_5c235853Workerbee(_input_params=self.map_dag_inputs)]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'), 'w') as out_file:
            out_file.write('done!\n')

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'))
        }


class DaylightFactorRayTracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = self.input()['CreateRadFolder']['sensor_grids'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['CreateRadFolder']['sensor_grids'].path

    def run(self):
        yield [DaylightFactorRayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'), 'w') as out_file:
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
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'))
        }


class GenerateSky(QueenbeeTask):
    """Generates a sky with certain illuminance level."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    illuminance = luigi.Parameter(default='100000.0')

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
        return 'honeybee-radiance sky illuminance {illuminance} --name overcast.sky'.format(illuminance=self.illuminance)

    def output(self):
        return {
            'sky': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/100000_lux.sky')
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky', 'from': 'overcast.sky',
                'to': os.path.join(self.execution_folder, 'resources/100000_lux.sky')
            }]


class _Main_5c235853Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [DaylightFactorRayTracing(_input_params=self.input_values)]
