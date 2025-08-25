"""
This file is auto-generated from annual-daylight:0.10.20.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.annual_daylight_ray_tracing import _AnnualDaylightRayTracing_e6056798Orchestrator as AnnualDaylightRayTracing_e6056798Workerbee
from .dependencies.annual_daylight_post_process import _AnnualDaylightPostProcess_e6056798Orchestrator as AnnualDaylightPostProcess_e6056798Workerbee
from .dependencies.annual_daylight_prepare_folder import _AnnualDaylightPrepareFolder_e6056798Orchestrator as AnnualDaylightPrepareFolder_e6056798Workerbee


_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'grid_metrics': None,
    'min_sensor_count': 1000,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05 -dr 0',
    'schedule': None,
    'simulation_folder': '.',
    'thresholds': '-t 300 -lt 100 -ut 3000',
    'timestep': 1,
    'wea': None}


class PrepareFolderAnnualDaylight(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
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
            'north': self.north,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'grid_filter': self.grid_filter,
            'model': self.model,
            'wea': self.wea,
            'timestep': self.timestep
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [AnnualDaylightPrepareFolder_e6056798Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder_annual_daylight.done').write_text('done!')

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources').resolve().as_posix()
            ),
            
            'results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'resources/grid/_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder_annual_daylight.done').resolve().as_posix())
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
                'name': 'results', 'from': 'results',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'resources/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'resources/grid/_info.json').resolve().as_posix()}]


class AnnualDaylightRaytracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def thresholds(self):
        return self._input_params['thresholds']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['model_folder'].path, 'bsdf')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['results'].path, 'sun-up-hours.txt')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def schedule(self):
        try:
            pathlib.Path(self._input_params['schedule'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['schedule'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def study_info(self):
        try:
            pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['results'].path, 'study_info.json')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['results'].path, 'study_info.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results').resolve().as_posix()

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
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_matrix': self.sky_matrix,
            'sky_dome': self.sky_dome,
            'bsdfs': self.bsdfs,
            'sun_up_hours': self.sun_up_hours,
            'schedule': self.schedule,
            'thresholds': self.thresholds,
            'study_info': self.study_info
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [AnnualDaylightRayTracing_e6056798Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'annual_daylight_raytracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'annual_daylight_raytracing.done').resolve().as_posix())
        }


class AnnualDaylightRaytracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolderAnnualDaylight']['sensor_grids'].path

    def run(self):
        yield [AnnualDaylightRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'annual_daylight_raytracing.done')
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
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'annual_daylight_raytracing.done').resolve().as_posix())
        }


class PostProcessAnnualDaylight(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def initial_results(self):
        value = pathlib.Path('initial_results/metrics')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dist_info(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'grid/_redist_info.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grids_info(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['results'].path, 'grids_info.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid_metrics(self):
        try:
            pathlib.Path(self._input_params['grid_metrics'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['grid_metrics'])
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
            'initial_results': self.initial_results,
            'dist_info': self.dist_info,
            'grids_info': self.grids_info,
            'model': self.model,
            'grid_metrics': self.grid_metrics
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [AnnualDaylightPostProcess_e6056798Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'post_process_annual_daylight.done').write_text('done!')

    def requires(self):
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params), 'AnnualDaylightRaytracing': AnnualDaylightRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'post_process_annual_daylight.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class RestructureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'ill'

    as_text = luigi.Parameter(default='False')

    delimiter = luigi.Parameter(default='tab')

    fmt = luigi.Parameter(default='%.2f')

    output_extension = luigi.Parameter(default='ill')

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/final')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dist_info(self):
        try:
            pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'grid/_redist_info.json')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'grid/_redist_info.json')
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
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json --output-extension {output_extension} --as-text {as_text} --fmt {fmt} --delimiter {delimiter}'.format(extension=self.extension, fmt=self.fmt, output_extension=self.output_extension, delimiter=self.delimiter, as_text=self.as_text)

    def requires(self):
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params), 'AnnualDaylightRaytracing': AnnualDaylightRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/__static_apertures__/default/total').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False},
            {'name': 'dist_info', 'to': 'dist_info.json', 'from': self.dist_info, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results/__static_apertures__/default/total').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension,
            'as_text': self.as_text,
            'delimiter': self.delimiter,
            'fmt': self.fmt,
            'output_extension': self.output_extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _Main_e6056798Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [PostProcessAnnualDaylight(_input_params=self.input_values), RestructureResults(_input_params=self.input_values)]
