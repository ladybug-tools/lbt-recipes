"""
This file is auto-generated from annual-energy-use:0.5.3.
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
    'measures': None,
    'model': None,
    'params_folder': '__params',
    'sim_par': None,
    'simulation_folder': '.',
    'units': 'si',
    'viz_variables': ''}


class RunSimulation(QueenbeeTask):
    """Simulate a Model JSON file in EnergyPlus."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def report_units(self):
        return self._input_params['units']

    @property
    def viz_variables(self):
        return self._input_params['viz_variables']

    additional_string = luigi.Parameter(default='')

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
    def sim_par(self):
        try:
            pathlib.Path(self._input_params['sim_par'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['sim_par'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def measures(self):
        try:
            pathlib.Path(self._input_params['measures'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['measures'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def additional_idf(self):
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

    def command(self):
        return 'honeybee-energy simulate model model.hbjson weather.epw --sim-par-json sim-par.json --measures measures --additional-string "{additional_string}" --additional-idf additional.idf --report-units {report_units} --folder output {viz_variables}'.format(report_units=self.report_units, additional_string=self.additional_string, viz_variables=self.viz_variables)

    def output(self):
        return {
            'hbjson': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model.hbjson').resolve().as_posix()
            ),
            
            'result_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'run').resolve().as_posix()
            ),
            
            'result_report': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results.html').resolve().as_posix()
            ),
            
            'visual_report': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visual.html').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False},
            {'name': 'ddy', 'to': 'weather.ddy', 'from': self.ddy, 'optional': True},
            {'name': 'sim_par', 'to': 'sim-par.json', 'from': self.sim_par, 'optional': True},
            {'name': 'measures', 'to': 'measures', 'from': self.measures, 'optional': True},
            {'name': 'additional_idf', 'to': 'additional.idf', 'from': self.additional_idf, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'hbjson', 'from': 'output/in.hbjson',
                'to': pathlib.Path(self.execution_folder, 'model.hbjson').resolve().as_posix(),
                'optional': True,
                'type': 'file'
            },
                
            {
                'name': 'result-folder', 'from': 'output/run',
                'to': pathlib.Path(self.execution_folder, 'run').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'result-report', 'from': 'output/reports/openstudio_results_report.html',
                'to': pathlib.Path(self.execution_folder, 'results.html').resolve().as_posix(),
                'optional': True,
                'type': 'file'
            },
                
            {
                'name': 'visual-report', 'from': 'output/reports/view_data_report.html',
                'to': pathlib.Path(self.execution_folder, 'visual.html').resolve().as_posix(),
                'optional': True,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.99.1'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class ComputeEui(QueenbeeTask):
    """Get information about energy use intensity from energy simulation SQLite files."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def units(self):
        return self._input_params['units']

    @property
    def result_folder(self):
        value = pathlib.Path(self.input()['RunSimulation']['result_folder'].path)
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
        return 'honeybee-energy result energy-use-intensity result_folder --{units} --output-file output.json'.format(units=self.units)

    def requires(self):
        return {'RunSimulation': RunSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'eui_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'eui.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_folder', 'to': 'result_folder', 'from': self.result_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'eui-json', 'from': 'output.json',
                'to': pathlib.Path(self.execution_folder, 'eui.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.99.1'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _Main_72fa8a0eOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [ComputeEui(_input_params=self.input_values)]
