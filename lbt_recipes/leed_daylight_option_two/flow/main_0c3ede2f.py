"""
This file is auto-generated from leed-daylight-option-two:0.3.10.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    pollination: info@pollination.solutions

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.leed_daylight_option_two_visualization import _LeedDaylightOptionTwoVisualization_0c3ede2fOrchestrator as LeedDaylightOptionTwoVisualization_0c3ede2fWorkerbee
from .dependencies.point_in_time_grid_entry_point import _PointInTimeGridEntryPoint_0c3ede2fOrchestrator as PointInTimeGridEntryPoint_0c3ede2fWorkerbee
from .dependencies.leed_daylight_option_two_prepare_folder import _LeedDaylightOptionTwoPrepareFolder_0c3ede2fOrchestrator as LeedDaylightOptionTwoPrepareFolder_0c3ede2fWorkerbee


_default_inputs = {   'cpu_count': 50,
    'glare_control_devices': 'glare-control',
    'grid_filter': '*',
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 5 -aa 0.1 -ad 2048 -ar 64',
    'simulation_folder': '.',
    'wea': None}


class PrepareFolder(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def north(self):
        return self._input_params['north']

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
            'model': self.model,
            'wea': self.wea,
            'grid_filter': self.grid_filter,
            'north': self.north
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [LeedDaylightOptionTwoPrepareFolder_0c3ede2fWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder.done').write_text('done!')

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources').resolve().as_posix()
            ),
            
            'simulation': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'simulation').resolve().as_posix()
            ),
            'sky_list': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'resources/skies/sky_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder.done').resolve().as_posix())
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
                'name': 'simulation', 'from': 'simulation',
                'to': pathlib.Path(self.execution_folder, 'simulation').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sky-list', 'from': 'resources/skies/sky_info.json', 'to': pathlib.Path(self.params_folder, 'resources/skies/sky_info.json').resolve().as_posix()}]


class IlluminanceSimulationLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def model_folder(self):
        value = pathlib.Path(self.input()['PrepareFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['PrepareFolder']['resources'].path, 'skies/{item_path}'.format(item_path=self.item['path']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grids_file(self):
        value = pathlib.Path(self.input()['PrepareFolder']['resources'].path, 'grids_info.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['PrepareFolder']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolder']['model_folder'].path, 'bsdf')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'simulation/{item_id}'.format(item_id=self.item['id'])).resolve().as_posix()

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
            'model_folder': self.model_folder,
            'sky': self.sky,
            'sensor_grids_file': self.sensor_grids_file,
            'grid_filter': self.grid_filter,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'radiance_parameters': self.radiance_parameters,
            'bsdfs': self.bsdfs
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [PointInTimeGridEntryPoint_0c3ede2fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'illuminance_simulation.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'illuminance_simulation.done').resolve().as_posix())
        }


class IlluminanceSimulation(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sky_list(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sky_list'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sky_list)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['sky_list'].path

    def run(self):
        yield [IlluminanceSimulationLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'illuminance_simulation.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'illuminance_simulation.done').resolve().as_posix())
        }


class EvaluateCredits(QueenbeeTask):
    """Estimate LEED daylight credits from two point-in-time illuminance folders."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def glare_control_devices(self):
        return self._input_params['glare_control_devices']

    @property
    def folder(self):
        value = pathlib.Path(self.input()['PrepareFolder']['simulation'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'evaluate_credits.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance post-process leed-illuminance raw_results --{glare_control_devices} --sub-folder ../pass_fail --output-file credit_summary.json'.format(glare_control_devices=self.glare_control_devices)

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'IlluminanceSimulation': IlluminanceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'pass_fail_results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            ),
            
            'credit_summary': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'credit_summary.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'pass-fail-results', 'from': 'pass_fail',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'credit-summary', 'from': 'credit_summary.json',
                'to': pathlib.Path(self.execution_folder, 'credit_summary.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'glare_control_devices': self.glare_control_devices}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.268'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateVisualization(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def illuminance_9am(self):
        value = pathlib.Path('simulation/9AM/results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def illuminance_3pm(self):
        value = pathlib.Path('simulation/3PM/results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def pass_fail_9am(self):
        value = pathlib.Path('results/9AM')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def pass_fail_3pm(self):
        value = pathlib.Path('results/3PM')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def pass_fail_combined(self):
        value = pathlib.Path('results/combined')
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
            'illuminance_9am': self.illuminance_9am,
            'illuminance_3pm': self.illuminance_3pm,
            'pass_fail_9am': self.pass_fail_9am,
            'pass_fail_3pm': self.pass_fail_3pm,
            'pass_fail_combined': self.pass_fail_combined
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [LeedDaylightOptionTwoVisualization_0c3ede2fWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'create_visualization.done').write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'IlluminanceSimulation': IlluminanceSimulation(_input_params=self._input_params), 'EvaluateCredits': EvaluateCredits(_input_params=self._input_params)}

    def output(self):
        return {
            'visualization': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'create_visualization.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'visualization', 'from': 'visualization.vsf',
                'to': pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _Main_0c3ede2fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateVisualization(_input_params=self.input_values)]
