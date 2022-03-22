"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param


_default_inputs = {   'air_speed_mtx': None,
    'comfort_parameters': '--cold 9 --heat 26',
    'direct_irradiance': None,
    'enclosure_info': None,
    'epw': None,
    'grid_name': None,
    'indirect_irradiance': None,
    'modifiers': None,
    'occ_schedules': None,
    'params_folder': '__params',
    'ref_irradiance': None,
    'result_sql': None,
    'run_period': '',
    'schedule': None,
    'simulation_folder': '.',
    'solarcal_parameters': '--posture standing --sharp 135 --absorptivity 0.7 '
                           '--emissivity 0.95',
    'sun_up_hours': None,
    'view_factors': None,
    'wind_speed': None}


class ComputeTcp(QueenbeeTask):
    """Compute Thermal Comfort Petcent (TCP) from thermal condition CSV map."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def condition_csv(self):
        value = pathlib.Path(self.input()['ProcessUtciMatrix']['condition_map'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path(self._input_params['enclosure_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def occ_schedule_json(self):
        value = pathlib.Path(self._input_params['occ_schedules'])
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
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'ladybug-comfort map tcp condition.csv enclosure_info.json --schedule schedule.txt --occ-schedule-json occ_schedule.json --folder output'

    def requires(self):
        return {'ProcessUtciMatrix': ProcessUtciMatrix(_input_params=self._input_params)}

    def output(self):
        return {
            'tcp': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP/{name}.csv'.format(name=self.name)).resolve().as_posix()
            ),
            
            'hsp': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP/{name}.csv'.format(name=self.name)).resolve().as_posix()
            ),
            
            'csp': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'condition_csv', 'to': 'condition.csv', 'from': self.condition_csv, 'optional': False},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info, 'optional': False},
            {'name': 'occ_schedule_json', 'to': 'occ_schedule.json', 'from': self.occ_schedule_json, 'optional': False},
            {'name': 'schedule', 'to': 'schedule.txt', 'from': self.schedule, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'tcp', 'from': 'output/tcp.csv',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'hsp', 'from': 'output/hsp.csv',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'csp', 'from': 'output/csp.csv',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateAirSpeedJson(QueenbeeTask):
    """Get a JSON of air speeds that can be used as input for the mtx functions."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def multiply_by(self):
        return '1.0'

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path(self._input_params['enclosure_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def outdoor_air_speed(self):
        try:
            pathlib.Path(self._input_params['wind_speed'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['wind_speed'])
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
        return 'ladybug-comfort epw air-speed-json weather.epw enclosure_info.json --multiply-by {multiply_by} --indoor-air-speed in_speed.txt --outdoor-air-speed out_speed.txt --run-period "{run_period}" --output-file air_speed.json'.format(multiply_by=self.multiply_by, run_period=self.run_period)

    def output(self):
        return {
            'air_speeds': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'conditions/air_speed/{name}.json'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info, 'optional': False},
            {'name': 'outdoor_air_speed', 'to': 'out_speed.txt', 'from': self.outdoor_air_speed, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'air-speeds', 'from': 'air_speed.json',
                'to': pathlib.Path(self.execution_folder, 'conditions/air_speed/{name}.json'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateAirTemperatureMap(QueenbeeTask):
    """Get CSV files with maps of air temperatures or humidity from EnergyPlus results."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def metric(self):
        return 'air-temperature'

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def result_sql(self):
        value = pathlib.Path(self._input_params['result_sql'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path(self._input_params['enclosure_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

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

    def command(self):
        return 'ladybug-comfort map air result.sql enclosure_info.json weather.epw --run-period "{run_period}" --{metric} --output-file air.csv'.format(run_period=self.run_period, metric=self.metric)

    def output(self):
        return {
            'air_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'conditions/air_temperature/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_sql', 'to': 'result.sql', 'from': self.result_sql, 'optional': False},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'air-map', 'from': 'air.csv',
                'to': pathlib.Path(self.execution_folder, 'conditions/air_temperature/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateLongwaveMrtMap(QueenbeeTask):
    """Get CSV files with maps of longwave MRT from Radiance and EnergyPlus results."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def result_sql(self):
        value = pathlib.Path(self._input_params['result_sql'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_factors(self):
        value = pathlib.Path(self._input_params['view_factors'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def modifiers(self):
        value = pathlib.Path(self._input_params['modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path(self._input_params['enclosure_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

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

    def command(self):
        return 'ladybug-comfort map longwave-mrt result.sql view_factors.csv view_factors.mod enclosure_info.json weather.epw --run-period "{run_period}" --output-file longwave.csv'.format(run_period=self.run_period)

    def output(self):
        return {
            'longwave_mrt_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'conditions/longwave_mrt/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_sql', 'to': 'result.sql', 'from': self.result_sql, 'optional': False},
            {'name': 'view_factors', 'to': 'view_factors.csv', 'from': self.view_factors, 'optional': False},
            {'name': 'modifiers', 'to': 'view_factors.mod', 'from': self.modifiers, 'optional': False},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'longwave-mrt-map', 'from': 'longwave.csv',
                'to': pathlib.Path(self.execution_folder, 'conditions/longwave_mrt/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateRelHumidityMap(QueenbeeTask):
    """Get CSV files with maps of air temperatures or humidity from EnergyPlus results."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def metric(self):
        return 'relative-humidity'

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def result_sql(self):
        value = pathlib.Path(self._input_params['result_sql'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path(self._input_params['enclosure_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

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

    def command(self):
        return 'ladybug-comfort map air result.sql enclosure_info.json weather.epw --run-period "{run_period}" --{metric} --output-file air.csv'.format(run_period=self.run_period, metric=self.metric)

    def output(self):
        return {
            'air_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'conditions/rel_humidity/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_sql', 'to': 'result.sql', 'from': self.result_sql, 'optional': False},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'air-map', 'from': 'air.csv',
                'to': pathlib.Path(self.execution_folder, 'conditions/rel_humidity/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateShortwaveMrtMap(QueenbeeTask):
    """Get CSV files with maps of shortwave MRT Deltas from Radiance results."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def solarcal_par(self):
        return self._input_params['solarcal_parameters']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def name(self):
        return self._input_params['grid_name']

    indirect_is_total = luigi.Parameter(default='is-indirect')

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def indirect_irradiance(self):
        value = pathlib.Path(self._input_params['indirect_irradiance'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_irradiance(self):
        value = pathlib.Path(self._input_params['direct_irradiance'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_irradiance(self):
        value = pathlib.Path(self._input_params['ref_irradiance'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self._input_params['sun_up_hours'])
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
        return 'ladybug-comfort map shortwave-mrt weather.epw indirect.ill direct.ill ref.ill sun-up-hours.txt --contributions dynamic --solarcal-par "{solarcal_par}" --run-period "{run_period}" --{indirect_is_total} --output-file shortwave.csv'.format(solarcal_par=self.solarcal_par, run_period=self.run_period, indirect_is_total=self.indirect_is_total)

    def output(self):
        return {
            'shortwave_mrt_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'conditions/shortwave_mrt/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False},
            {'name': 'indirect_irradiance', 'to': 'indirect.ill', 'from': self.indirect_irradiance, 'optional': False},
            {'name': 'direct_irradiance', 'to': 'direct.ill', 'from': self.direct_irradiance, 'optional': False},
            {'name': 'ref_irradiance', 'to': 'ref.ill', 'from': self.ref_irradiance, 'optional': False},
            {'name': 'sun_up_hours', 'to': 'sun-up-hours.txt', 'from': self.sun_up_hours, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'shortwave-mrt-map', 'from': 'shortwave.csv',
                'to': pathlib.Path(self.execution_folder, 'conditions/shortwave_mrt/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class ProcessUtciMatrix(QueenbeeTask):
    """Get CSV files with matrices of UTCI comfort from matrices of UTCI inputs."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def comfort_par(self):
        return self._input_params['comfort_parameters']

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def air_temperature_mtx(self):
        value = pathlib.Path(self.input()['CreateAirTemperatureMap']['air_map'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def rel_humidity_mtx(self):
        value = pathlib.Path(self.input()['CreateRelHumidityMap']['air_map'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def rad_temperature_mtx(self):
        value = pathlib.Path(self.input()['CreateLongwaveMrtMap']['longwave_mrt_map'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def rad_delta_mtx(self):
        value = pathlib.Path(self.input()['CreateShortwaveMrtMap']['shortwave_mrt_map'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wind_speed_json(self):
        value = pathlib.Path(self.input()['CreateAirSpeedJson']['air_speeds'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def air_speed_mtx(self):
        try:
            pathlib.Path(self._input_params['air_speed_mtx'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['air_speed_mtx'])
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
        return 'ladybug-comfort mtx utci air_temperature.csv rel_humidity.csv --rad-temperature-mtx rad_temperature.csv --rad-delta-mtx rad_delta.csv --wind-speed-json wind_speed.json --air-speed-mtx air_speed.csv --comfort-par "{comfort_par}" --folder output'.format(comfort_par=self.comfort_par)

    def requires(self):
        return {'CreateLongwaveMrtMap': CreateLongwaveMrtMap(_input_params=self._input_params), 'CreateShortwaveMrtMap': CreateShortwaveMrtMap(_input_params=self._input_params), 'CreateAirTemperatureMap': CreateAirTemperatureMap(_input_params=self._input_params), 'CreateRelHumidityMap': CreateRelHumidityMap(_input_params=self._input_params), 'CreateAirSpeedJson': CreateAirSpeedJson(_input_params=self._input_params)}

    def output(self):
        return {
            'temperature_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature/{name}.csv'.format(name=self.name)).resolve().as_posix()
            ),
            
            'condition_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition/{name}.csv'.format(name=self.name)).resolve().as_posix()
            ),
            
            'category_map': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity/{name}.csv'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'air_temperature_mtx', 'to': 'air_temperature.csv', 'from': self.air_temperature_mtx, 'optional': False},
            {'name': 'rel_humidity_mtx', 'to': 'rel_humidity.csv', 'from': self.rel_humidity_mtx, 'optional': False},
            {'name': 'rad_temperature_mtx', 'to': 'rad_temperature.csv', 'from': self.rad_temperature_mtx, 'optional': False},
            {'name': 'rad_delta_mtx', 'to': 'rad_delta.csv', 'from': self.rad_delta_mtx, 'optional': False},
            {'name': 'wind_speed_json', 'to': 'wind_speed.json', 'from': self.wind_speed_json, 'optional': False},
            {'name': 'air_speed_mtx', 'to': 'air_speed.csv', 'from': self.air_speed_mtx, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'temperature-map', 'from': 'output/temperature.csv',
                'to': pathlib.Path(self.execution_folder, 'results/temperature/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'condition-map', 'from': 'output/condition.csv',
                'to': pathlib.Path(self.execution_folder, 'results/condition/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'category-map', 'from': 'output/condition_intensity.csv',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity/{name}.csv'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class _ComfortMappingEntryPoint_84dd66d2Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [ComputeTcp(_input_params=self.input_values)]
