"""
This file is auto-generated from well-daylight:0.0.21.
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


_default_inputs = {'epw': None, 'params_folder': '__params', 'simulation_folder': '.'}


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
            'daylight_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix()
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
                'name': 'daylight-hours', 'from': 'daylight_hours.csv',
                'to': pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.246'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateWea(QueenbeeTask):
    """Translate an .epw file to a .wea file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    period = luigi.Parameter(default='')

    timestep = luigi.Parameter(default='1')

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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_wea.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'ladybug translate epw-to-wea weather.epw --analysis-period "{period}" --timestep {timestep} --output-file weather.wea'.format(timestep=self.timestep, period=self.period)

    def output(self):
        return {
            'wea': luigi.LocalTarget(
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
                'name': 'wea', 'from': 'weather.wea',
                'to': pathlib.Path(self.execution_folder, 'wea.wea').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period,
            'timestep': self.timestep}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/ladybug:0.42.6'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _WellDaylightProcessEPW_1d5ef609Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateDaylightHours(_input_params=self.input_values), CreateWea(_input_params=self.input_values)]
