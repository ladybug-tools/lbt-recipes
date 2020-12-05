"""
Note: This file is auto-generated from a Queenbee recipe and should not be edited or
modified directly. Modify the original recipe instead and re-generate the files.
"""

import luigi
import os
from honeybee_radiance_recipe.recipe_helper import QueenbeeTask, load_input_param
from .dependencies.ray_tracing import _RayTracingOrchestrator as RayTracingWorkerbee


_default_inputs = {
    'model': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2',
    'sensor_count': 200,
    'simulation_folder': '.'
}


class AggregateResultsLoop(QueenbeeTask):
    """Merge several files into a single file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return 'grid'

    @property
    def extension(self):
        return '.res'

    @property
    def results_folder(self):
        value = 'initial_results/{item_name}/results'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

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
        return 'honeybee-radiance grid merge input_results grid {extension}'.format(extension=self.extension)

    def requires(self):
        return {'DaylightFactorRayTracing': DaylightFactorRayTracing(_input_params=self._input_params), 'CreateRadianceFolder': CreateRadianceFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/{item_name}.res'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'results_folder', 'to': 'input_results', 'from': self.results_folder}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'grid{extension}'.format(extension=self.extension),
                'to': os.path.join(self.execution_folder, 'results/{item_name}.res'.format(item_name=self.item['name']))
            }]


class AggregateResults(luigi.Task):
    """Merge several files into a single file."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = self.input()['CreateRadianceFolder']['sensor_grids'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['CreateRadianceFolder']['sensor_grids'].path

    def run(self):
        yield [AggregateResultsLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'aggregate_results.done'), 'w') as out_file:
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
        return {'DaylightFactorRayTracing': DaylightFactorRayTracing(_input_params=self._input_params), 'CreateRadianceFolder': CreateRadianceFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'aggregate_results.done'))
        }


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder and sky"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = self.input()['CreateRadianceFolder']['model_folder'].path.replace('\\', '/')
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
        return {'GenerateSky': GenerateSky(_input_params=self._input_params), 'CreateRadianceFolder': CreateRadianceFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/scene.oct')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': os.path.join(self.execution_folder, 'resources/scene.oct')
            }]


class CreateRadianceFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
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
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson'

    def output(self):
        return {

            'model_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'model')
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
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': os.path.join(self.execution_folder, 'model')
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
    def octree_file(self):
        value = self.input()['CreateOctree']['scene_file'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['CreateRadianceFolder']['model_folder'].path, 'grid/{item_name}.pts'.format(item_name=self.item['name'])).replace('\\', '/')
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
            'sensor_grid': self.sensor_grid
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [RayTracingWorkerbee(_input_params=self.map_dag_inputs)]
        with open(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'), 'w') as out_file:
            out_file.write('done!\n')

    def requires(self):
        return {'CreateRadianceFolder': CreateRadianceFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

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
        value = self.input()['CreateRadianceFolder']['sensor_grids'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['CreateRadianceFolder']['sensor_grids'].path

    def run(self):
        yield [DaylightFactorRayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
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
        return {'CreateRadianceFolder': CreateRadianceFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'daylight_factor_ray_tracing.done'))
        }


class GenerateSky(QueenbeeTask):
    """Generates a 100000 lux sky"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

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
        return 'honeybee-radiance sky illuminance 100000'

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
                'name': 'sky', 'from': '100000_lux.sky',
                'to': os.path.join(self.execution_folder, 'resources/100000_lux.sky')
            }]


class _MainOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [AggregateResults(_input_params=self.input_values)]
