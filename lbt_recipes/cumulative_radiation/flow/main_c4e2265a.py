"""
This file is auto-generated from cumulative-radiation:0.3.8.
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
from .dependencies.cumulative_radiation_postprocess import _CumulativeRadiationPostprocess_c4e2265aOrchestrator as CumulativeRadiationPostprocess_c4e2265aWorkerbee
from .dependencies.cumulative_radiation_prepare_folder import _CumulativeRadiationPrepareFolder_c4e2265aOrchestrator as CumulativeRadiationPrepareFolder_c4e2265aWorkerbee


_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'simulation_folder': '.',
    'sky_density': 1,
    'timestep': 1,
    'wea': None}


class PrepareFolderCumulativeRadiation(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def timestep(self):
        return self._input_params['timestep']

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
    def sky_density(self):
        return self._input_params['sky_density']

    radiance_parameters = luigi.Parameter(default='-ab 2 -ad 5000 -lw 2e-05')

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
            'timestep': self.timestep,
            'north': self.north,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'grid_filter': self.grid_filter,
            'sky_density': self.sky_density,
            'model': self.model,
            'wea': self.wea
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [CumulativeRadiationPrepareFolder_c4e2265aWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder_cumulative_radiation.done').write_text('done!')

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
            
            'initial_results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'resources/grid/_info.json').resolve().as_posix()
                ),
                'grids_info': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'results/average_irradiance/grids_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder_cumulative_radiation.done').resolve().as_posix())
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
            },
                
            {
                'name': 'initial-results', 'from': 'initial_results',
                'to': pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'resources/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'resources/grid/_info.json').resolve().as_posix()},
                {'name': 'grids-info', 'from': 'results/average_irradiance/grids_info.json', 'to': pathlib.Path(self.params_folder, 'results/average_irradiance/grids_info.json').resolve().as_posix()}]


class SkyRadiationRaytracingLoop(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1'

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def output_format(self):
        return 'a'

    header = luigi.Parameter(default='keep')

    order_by = luigi.Parameter(default='sensor')

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['resources'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['model_folder'].path, 'bsdf')
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
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by} --{header}-header'.format(output_format=self.output_format, order_by=self.order_by, sensor_count=self.sensor_count, fixed_radiance_parameters=self.fixed_radiance_parameters, radiance_parameters=self.radiance_parameters, conversion=self.conversion, header=self.header)

    def requires(self):
        return {'PrepareFolderCumulativeRadiation': PrepareFolderCumulativeRadiation(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
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


class SkyRadiationRaytracing(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolderCumulativeRadiation']['sensor_grids'].path

    def run(self):
        yield [SkyRadiationRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'sky_radiation_raytracing.done')
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
        return {'PrepareFolderCumulativeRadiation': PrepareFolderCumulativeRadiation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'sky_radiation_raytracing.done').resolve().as_posix())
        }

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.140'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'res'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results')
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
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'SkyRadiationRaytracing': SkyRadiationRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/average_irradiance').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results/average_irradiance').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.140'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CumulativeRadiationPostprocessLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def average_irradiance(self):
        value = pathlib.Path(self.input()['RestructureResults']['output_folder'].path, '{item_full_id}.res'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

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
            'grid_name': self.grid_name,
            'average_irradiance': self.average_irradiance,
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
        yield [CumulativeRadiationPostprocess_c4e2265aWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'cumulative_radiation_postprocess.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolderCumulativeRadiation': PrepareFolderCumulativeRadiation(_input_params=self._input_params), 'RestructureResults': RestructureResults(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'cumulative_radiation_postprocess.done').resolve().as_posix())
        }


class CumulativeRadiationPostprocess(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_info(self):
        value = pathlib.Path(self.input()['PrepareFolderCumulativeRadiation']['grids_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.grids_info)
        except:
            # it is a parameter
            return self.input()['PrepareFolderCumulativeRadiation']['grids_info'].path

    def run(self):
        yield [CumulativeRadiationPostprocessLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'cumulative_radiation_postprocess.done')
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
        return {'PrepareFolderCumulativeRadiation': PrepareFolderCumulativeRadiation(_input_params=self._input_params), 'RestructureResults': RestructureResults(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'cumulative_radiation_postprocess.done').resolve().as_posix())
        }


class _Main_c4e2265aOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CumulativeRadiationPostprocess(_input_params=self.input_values)]
