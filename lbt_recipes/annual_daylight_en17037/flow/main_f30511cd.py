"""
This file is auto-generated from annual-daylight-en17037:0.1.23.
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
from .dependencies.annual_daylight_e_n17037_post_process import _AnnualDaylightEN17037PostProcess_f30511cdOrchestrator as AnnualDaylightEN17037PostProcess_f30511cdWorkerbee
from .dependencies.main_b46ec90c import _Main_b46ec90cOrchestrator as Main_b46ec90cWorkerbee


_default_inputs = {   'cpu_count': 50,
    'epw': None,
    'grid_filter': '*',
    'grid_metrics': None,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'simulation_folder': '.',
    'thresholds': '-t 300 -lt 100 -ut 3000'}


class CreateDaylightHours(QueenbeeTask):
    """Convert EPW to EN 17037 schedule as a CSV file.
    
    This function generates a valid schedule for EN 17037, also known as daylight hours.
    Rather than a typical occupancy schedule, the daylight hours is half the year with
    the largest quantity of daylight."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_daylight_hours.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance schedule epw-to-daylight-hours weather.epw --name daylight_hours'

    def output(self):
        return {
            'daylight_hours_csv': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix()
            ),
            
            'daylight_hours_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'daylight_hours.json').resolve().as_posix()
            ),
            
            'daylight_hours_wea': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'wea.wea').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'daylight-hours-csv', 'from': 'daylight_hours.csv',
                'to': pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'daylight-hours-json', 'from': 'daylight_hours.json',
                'to': pathlib.Path(self.execution_folder, 'daylight_hours.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'daylight-hours-wea', 'from': 'daylight_hours.wea',
                'to': pathlib.Path(self.execution_folder, 'wea.wea').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.268'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RunTwoPhaseDaylightCoefficient(QueenbeeTask):
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
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    dtype = luigi.Parameter(default='float32')

    timestep = luigi.Parameter(default='1')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateDaylightHours']['daylight_hours_wea'].path)
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
            'radiance_parameters': self.radiance_parameters,
            'grid_filter': self.grid_filter,
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
        yield [Main_b46ec90cWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').write_text('done!')

    def requires(self):
        return {'CreateDaylightHours': CreateDaylightHours(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').resolve().as_posix())
        }


class AnnualMetricsEn17037Postprocess(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def thresholds(self):
        return self._input_params['thresholds']

    @property
    def results(self):
        value = pathlib.Path('results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def schedule(self):
        try:
            pathlib.Path(self.input()['CreateDaylightHours']['daylight_hours_csv'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateDaylightHours']['daylight_hours_csv'].path)
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
            'results': self.results,
            'schedule': self.schedule,
            'thresholds': self.thresholds,
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
        yield [AnnualDaylightEN17037PostProcess_f30511cdWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'annual_metrics_en17037_postprocess.done').write_text('done!')

    def requires(self):
        return {'CreateDaylightHours': CreateDaylightHours(_input_params=self._input_params), 'RunTwoPhaseDaylightCoefficient': RunTwoPhaseDaylightCoefficient(_input_params=self._input_params)}

    def output(self):
        return {
            'en17037': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'en17037').resolve().as_posix()
            ),
            
            'metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            ),
            
            'grid_summary': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'grid_summary.csv').resolve().as_posix()
            ),
            
            'visualization_en17037': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization_en17037.vsf').resolve().as_posix()
            ),
            
            'visualization_metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization_metrics.vsf').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'annual_metrics_en17037_postprocess.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'en17037', 'from': 'en17037',
                'to': pathlib.Path(self.execution_folder, 'en17037').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'grid-summary', 'from': 'grid_summary.csv',
                'to': pathlib.Path(self.execution_folder, 'grid_summary.csv').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'visualization-en17037', 'from': 'visualization_en17037.vsf',
                'to': pathlib.Path(self.execution_folder, 'visualization_en17037.vsf').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'visualization-metrics', 'from': 'visualization_metrics.vsf',
                'to': pathlib.Path(self.execution_folder, 'visualization_metrics.vsf').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _Main_f30511cdOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [AnnualMetricsEn17037Postprocess(_input_params=self.input_values)]
