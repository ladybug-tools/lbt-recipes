"""
This file is auto-generated from sky-view:1.2.6.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.sky_view_postprocess import _SkyViewPostprocess_961c2ad4Orchestrator as SkyViewPostprocess_961c2ad4Workerbee
from .dependencies.sky_view_prepare_folder import _SkyViewPrepareFolder_961c2ad4Orchestrator as SkyViewPrepareFolder_961c2ad4Workerbee


_default_inputs = {   'cloudy_sky': 'uniform',
    'cpu_count': 50,
    'grid_filter': '*',
    'min_sensor_count': 500,
    'model': None,
    'params_folder': '__params',
    'radiance_parameters': '-aa 0.1 -ad 2048 -ar 64',
    'simulation_folder': '.'}


class PrepareFolderSkyView(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def cloudy_sky(self):
        return self._input_params['cloudy_sky']

    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    radiance_parameters = luigi.Parameter(default='-aa 0.1 -ad 2048 -ar 64')

    @property
    def model(self):
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

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'model': self.model,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'cloudy_sky': self.cloudy_sky,
            'grid_filter': self.grid_filter
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [SkyViewPrepareFolder_961c2ad4Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder_sky_view.done').write_text('done!')

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources').resolve().as_posix()
            ),
            
            'initial_results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'resources/grid/_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder_sky_view.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'model').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'resources', 'from': 'resources',
                'to': pathlib.Path(self.execution_folder, 'resources').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'initial-results', 'from': 'initial_results',
                'to': pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'resources/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'resources/grid/_info.json').resolve().as_posix()}]


class SkyViewRayTracingLoop(QueenbeeTask):
    """Run ray-tracing and post-process the results for a skyview simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    fixed_radiance_parameters = luigi.Parameter(default='-I -ab 1 -h')

    @property
    def scene_file(self):
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid(self):
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['resources'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self.input()['PrepareFolderSkyView']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['model_folder'].path, 'bsdf')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_full_id}'.format(item_full_id=self.item['full_id'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --output grid.res'.format(radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def requires(self):
        return {'PrepareFolderSkyView': PrepareFolderSkyView(_input_params=self._input_params)}

    def output(self):
        return {
            'result': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'grid', 'to': 'grid.pts', 'from': self.grid, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result', 'from': 'grid.res',
                'to': pathlib.Path(self.execution_folder, '../{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.140'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class SkyViewRayTracing(luigi.Task):
    """Run ray-tracing and post-process the results for a skyview simulation."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolderSkyView']['sensor_grids'].path

    def run(self):
        yield [SkyViewRayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'sky_view_ray_tracing.done')
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
        return {'PrepareFolderSkyView': PrepareFolderSkyView(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'sky_view_ray_tracing.done').resolve().as_posix())
        }

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.140'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class PostprocessSkyView(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def input_folder(self):
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['initial_results'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grids_info(self):
        value = pathlib.Path(self.input()['PrepareFolderSkyView']['resources'].path, 'grids_info.json')
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

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'input_folder': self.input_folder,
            'grids_info': self.grids_info
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [SkyViewPostprocess_961c2ad4Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'postprocess_sky_view.done').write_text('done!')

    def requires(self):
        return {'PrepareFolderSkyView': PrepareFolderSkyView(_input_params=self._input_params), 'SkyViewRayTracing': SkyViewRayTracing(_input_params=self._input_params)}

    def output(self):
        return {
            'results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'postprocess_sky_view.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results', 'from': 'results',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _Main_961c2ad4Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [PostprocessSkyView(_input_params=self.input_values)]
