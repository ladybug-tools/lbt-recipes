"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask


_default_inputs = {   'bsdfs': None,
    'grid_name': None,
    'octree_file': None,
    'params_folder': '__params',
    'sensor_count': None,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sun_modifiers': None,
    'timestep': 1}


class CalculateCumulativeHours(QueenbeeTask):
    """Postprocess a Radiance matrix and add all the numbers in each row.

    This function is useful for translating Radiance results to outputs like radiation
    to total radiation. Input matrix must be in ASCII format. The header in the input
    file will be ignored."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def grid_name(self):
        return self._input_params['grid_name']

    @property
    def divisor(self):
        return self._input_params['timestep']

    @property
    def input_mtx(self):
        value = pathlib.Path(self.input()['ConvertToSunHours']['output_mtx'].path)
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
        return 'honeybee-radiance post-process sum-row input.mtx --divisor {divisor} --output sum.mtx'.format(divisor=self.divisor)

    def requires(self):
        return {'ConvertToSunHours': ConvertToSunHours(_input_params=self._input_params)}

    def output(self):
        return {
            'output_mtx': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../cumulative/{grid_name}.res'.format(grid_name=self.grid_name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_mtx', 'to': 'input.mtx', 'from': self.input_mtx, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-mtx', 'from': 'sum.mtx',
                'to': pathlib.Path(self.execution_folder, '../cumulative/{grid_name}.res'.format(grid_name=self.grid_name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class ConvertToSunHours(QueenbeeTask):
    """Convert a Radiance matrix to a new matrix with 0-1 values."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def grid_name(self):
        return self._input_params['grid_name']

    @property
    def minimum(self):
        return '0'

    @property
    def include_min(self):
        return 'exclude'

    include_max = luigi.Parameter(default='include')

    maximum = luigi.Parameter(default='1e+100')

    reverse = luigi.Parameter(default='comply')

    @property
    def input_mtx(self):
        value = pathlib.Path(self.input()['DirectIrradianceCalculation']['result_file'].path)
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
        return 'honeybee-radiance post-process convert-to-binary input.mtx --output binary.mtx --maximum {maximum} --minimum {minimum} --{reverse} --{include_min}-min --{include_max}-max'.format(maximum=self.maximum, minimum=self.minimum, reverse=self.reverse, include_min=self.include_min, include_max=self.include_max)

    def requires(self):
        return {'DirectIrradianceCalculation': DirectIrradianceCalculation(_input_params=self._input_params)}

    def output(self):
        return {
            'output_mtx': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../direct_sun_hours/{grid_name}.ill'.format(grid_name=self.grid_name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_mtx', 'to': 'input.mtx', 'from': self.input_mtx, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-mtx', 'from': 'binary.mtx',
                'to': pathlib.Path(self.execution_folder, '../direct_sun_hours/{grid_name}.ill'.format(grid_name=self.grid_name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class DirectIrradianceCalculation(QueenbeeTask):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers
    using rcontrib command."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -faa -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0'

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def grid_name(self):
        return self._input_params['grid_name']

    calculate_values = luigi.Parameter(default='value')

    order_by = luigi.Parameter(default='sensor')

    output_format = luigi.Parameter(default='a')

    radiance_parameters = luigi.Parameter(default='')

    @property
    def modifiers(self):
        value = pathlib.Path(self._input_params['sun_modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self._input_params['bsdfs'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['bsdfs'])
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
        return 'honeybee-radiance dc scontrib scene.oct grid.pts suns.mod --{calculate_values} --sensor-count {sensor_count} --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --output results.ill --order-by-{order_by}'.format(calculate_values=self.calculate_values, sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, conversion=self.conversion, output_format=self.output_format, order_by=self.order_by)

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{grid_name}.ill'.format(grid_name=self.grid_name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifiers', 'to': 'suns.mod', 'from': self.modifiers, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, '{grid_name}.ill'.format(grid_name=self.grid_name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class _DirectSunHoursCalculation_e39a9104Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CalculateCumulativeHours(_input_params=self.input_values)]
