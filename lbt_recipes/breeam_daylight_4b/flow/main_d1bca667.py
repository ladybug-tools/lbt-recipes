"""
This file is auto-generated from breeam-daylight-4b:1.0.9.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mikkel: mikkel@ladybug.tools
    pollination: info@pollination.solutions

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.breeam_daylight4b_visualization import _BreeamDaylight4bVisualization_d1bca667Orchestrator as BreeamDaylight4bVisualization_d1bca667Workerbee
from .dependencies.main_c3773f23 import _Main_c3773f23Orchestrator as Main_c3773f23Workerbee


_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05 -dr 0',
    'simulation_folder': '.',
    'wea': None}


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
        yield [Main_c3773f23Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').write_text('done!')

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').resolve().as_posix())
        }


class BreemDaylight4b(QueenbeeTask):
    """Calculate credits for BREEAM 4b."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def folder(self):
        value = pathlib.Path('results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def model(self):
        try:
            pathlib.Path(self._input_params['model'])
        except TypeError:
            # optional artifact
            return None
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
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'breem_daylight_4b.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess post-process breeam breeam-4b results --model-file model.hbjson --sub-folder breeam_summary'

    def requires(self):
        return {'RunTwoPhaseDaylightCoefficient': RunTwoPhaseDaylightCoefficient(_input_params=self._input_params)}

    def output(self):
        return {
            'breeam_summary': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'breeam_summary').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'results', 'from': self.folder, 'optional': False},
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'breeam-summary', 'from': 'breeam_summary',
                'to': pathlib.Path(self.execution_folder, 'breeam_summary').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/lbt-honeybee:0.8.438'

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
    def pass_fail(self):
        value = pathlib.Path(self.input()['BreemDaylight4b']['breeam_summary'].path, 'pass_fail')
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
            'pass_fail': self.pass_fail
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [BreeamDaylight4bVisualization_d1bca667Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'create_visualization.done').write_text('done!')

    def requires(self):
        return {'RunTwoPhaseDaylightCoefficient': RunTwoPhaseDaylightCoefficient(_input_params=self._input_params), 'BreemDaylight4b': BreemDaylight4b(_input_params=self._input_params)}

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


class _Main_d1bca667Orchestrator(luigi.WrapperTask):
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
