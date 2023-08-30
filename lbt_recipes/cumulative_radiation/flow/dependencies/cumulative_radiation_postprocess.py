"""
This file is auto-generated from cumulative-radiation:0.3.9.
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


_default_inputs = {   'average_irradiance': None,
    'grid_name': None,
    'params_folder': '__params',
    'simulation_folder': '.',
    'timestep': 1,
    'wea': None}


class AccumulateResults(QueenbeeTask):
    """Postprocess average irradiance (W/m2) into cumulative radiation (kWh/m2)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def average_irradiance(self):
        value = pathlib.Path(self._input_params['average_irradiance'])
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
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'accumulate_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance post-process cumulative-radiation avg_irr.mtx weather.wea --timestep {timestep} --output radiation.mtx'.format(timestep=self.timestep)

    def output(self):
        return {
            'radiation': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/cumulative_radiation/{name}.res'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'average_irradiance', 'to': 'avg_irr.mtx', 'from': self.average_irradiance, 'optional': False},
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'radiation', 'from': 'radiation.mtx',
                'to': pathlib.Path(self.execution_folder, 'results/cumulative_radiation/{name}.res'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'timestep': self.timestep}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.32'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _CumulativeRadiationPostprocess_49ddb174Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [AccumulateResults(_input_params=self.input_values)]
