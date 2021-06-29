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
import pathlib
from queenbee_local import QueenbeeTask
from .dependencies.daylight_factor_ray_tracing import _DaylightFactorRayTracing_e548dc8eOrchestrator as DaylightFactorRayTracing_e548dc8eWorkerbee


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
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['GenerateSky']['sky'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'GenerateSky': GenerateSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix(),
                'optional': False
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
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'bsdf_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            ),
            
            'model_sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/grid/_info.json').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'model').resolve().as_posix(),
                'optional': False
            },
                
            {
                'name': 'bsdf-folder', 'from': 'model/bsdf',
                'to': pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix(),
                'optional': False
            },
                
            {
                'name': 'model-sensor-grids-file', 'from': 'model/grid/_model_grids_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix(),
                'optional': False
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'model/grid/_info.json').resolve().as_posix()}]


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
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'sensor_count': self.sensor_count,
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'bsdfs': self.bsdfs
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DaylightFactorRayTracing_e548dc8eWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'daylight_factor_ray_tracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'daylight_factor_ray_tracing.done').resolve().as_posix())
        }


class DaylightFactorRayTracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path).as_posix()

    def run(self):
        yield [DaylightFactorRayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'daylight_factor_ray_tracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'daylight_factor_ray_tracing.done').resolve().as_posix())
        }


class GenerateSky(QueenbeeTask):
    """Generates a sky with certain illuminance level."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    illuminance = luigi.Parameter(default='100000.0')

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky illuminance {illuminance} --name overcast.sky'.format(illuminance=self.illuminance)

    def output(self):
        return {
            'sky': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/100000_lux.sky').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky', 'from': 'overcast.sky',
                'to': pathlib.Path(self.execution_folder, 'resources/100000_lux.sky').resolve().as_posix(),
                'optional': False
            }]


class _Main_e548dc8eOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [DaylightFactorRayTracing(_input_params=self.input_values)]
