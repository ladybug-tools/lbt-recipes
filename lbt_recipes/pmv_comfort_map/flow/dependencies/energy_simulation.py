"""
This file is auto-generated from pmv-comfort-map:0.8.18.
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


_default_inputs = {   'additional_idf': None,
    'ddy': None,
    'epw': None,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'run_period': '',
    'simulation_folder': '.'}


class CreateSimPar(QueenbeeTask):
    """Get a SimulationParameter JSON with all outputs for thermal comfort mapping."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def north(self):
        return self._input_params['north']

    building_type = luigi.Parameter(default='')

    climate_zone = luigi.Parameter(default='')

    efficiency_standard = luigi.Parameter(default='')

    filter_des_days = luigi.Parameter(default='filter-des-days')

    reporting_frequency = luigi.Parameter(default='Hourly')

    @property
    def ddy(self):
        try:
            pathlib.Path(self._input_params['ddy'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['ddy'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_sim_par.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy settings comfort-sim-par input.ddy --run-period "{run_period}" --north {north} --{filter_des_days} --output-file sim_par.json'.format(filter_des_days=self.filter_des_days, north=self.north, run_period=self.run_period)

    def output(self):
        return {
            'sim_par_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/simulation_parameter.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'ddy', 'to': 'input.ddy', 'from': self.ddy, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sim-par-json', 'from': 'sim_par.json',
                'to': pathlib.Path(self.execution_folder, 'energy/simulation_parameter.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'run_period': self.run_period,
            'north': self.north,
            'building_type': self.building_type,
            'climate_zone': self.climate_zone,
            'efficiency_standard': self.efficiency_standard,
            'filter_des_days': self.filter_des_days,
            'reporting_frequency': self.reporting_frequency}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.106.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class DynamicConstructionOutputs(QueenbeeTask):
    """Get an IDF file that requests transmittance outputs for dynamic windows."""

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
    def base_idf(self):
        try:
            pathlib.Path(self._input_params['additional_idf'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['additional_idf'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'dynamic_construction_outputs.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy settings dynamic-window-outputs model.json --base-idf base.idf --output-file base.idf'

    def output(self):
        return {
            'dynamic_out_idf': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/additional.idf').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False},
            {'name': 'base_idf', 'to': 'base.idf', 'from': self.base_idf, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dynamic-out-idf', 'from': 'base.idf',
                'to': pathlib.Path(self.execution_folder, 'energy/additional.idf').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.106.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RunEnergySimulation(QueenbeeTask):
    """Simulate a Model JSON file in EnergyPlus."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    additional_string = luigi.Parameter(default='')

    report_units = luigi.Parameter(default='none')

    viz_variables = luigi.Parameter(default='')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sim_par(self):
        try:
            pathlib.Path(self.input()['CreateSimPar']['sim_par_json'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateSimPar']['sim_par_json'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def additional_idf(self):
        try:
            pathlib.Path(self.input()['DynamicConstructionOutputs']['dynamic_out_idf'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['DynamicConstructionOutputs']['dynamic_out_idf'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'run_energy_simulation.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy simulate model model.hbjson weather.epw --sim-par-json sim-par.json --measures measures --additional-string "{additional_string}" --additional-idf additional.idf --report-units {report_units} --folder output {viz_variables}'.format(viz_variables=self.viz_variables, report_units=self.report_units, additional_string=self.additional_string)

    def requires(self):
        return {'CreateSimPar': CreateSimPar(_input_params=self._input_params), 'DynamicConstructionOutputs': DynamicConstructionOutputs(_input_params=self._input_params)}

    def output(self):
        return {
            'sql': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/eplusout.sql').resolve().as_posix()
            ),
            
            'idf': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/in.idf').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False},
            {'name': 'sim_par', 'to': 'sim-par.json', 'from': self.sim_par, 'optional': True},
            {'name': 'additional_idf', 'to': 'additional.idf', 'from': self.additional_idf, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sql', 'from': 'output/run/eplusout.sql',
                'to': pathlib.Path(self.execution_folder, 'energy/eplusout.sql').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'idf', 'from': 'output/run/in.idf',
                'to': pathlib.Path(self.execution_folder, 'energy/in.idf').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'additional_string': self.additional_string,
            'report_units': self.report_units,
            'viz_variables': self.viz_variables}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.106.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _EnergySimulation_73edd45fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [RunEnergySimulation(_input_params=self.input_values)]
