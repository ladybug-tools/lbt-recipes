"""
This file is auto-generated from utci-comfort-map:0.9.15.
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


_default_inputs = {   'air_speed_matrices': None,
    'cpu_count': 50,
    'epw': None,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'run_period': '',
    'simulation_folder': '.'}


class CreateModelOccSchedules(QueenbeeTask):
    """Translate a Model's occupancy schedules into a JSON of 0/1 values.

    This JSON is useful in workflows that compute thermal comfort percent,
    daylight autonomy, etc."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    threshold = luigi.Parameter(default='0.1')

    @property
    def model(self):
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_model_occ_schedules.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy translate model-occ-schedules model.json --threshold {threshold} --period "{period}" --output-file occ_schedules.json'.format(threshold=self.threshold, period=self.period)

    def output(self):
        return {
            'occ_schedule_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/occupancy_schedules.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'occ-schedule-json', 'from': 'occ_schedules.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/occupancy_schedules.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period,
            'threshold': self.threshold}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.106.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateModelTransSchedules(QueenbeeTask):
    """Translate Model shade transmittance schedules into a JSON of fractional values."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    @property
    def model(self):
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_model_trans_schedules.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy translate model-transmittance-schedules model.json --period "{period}" --output-file trans_schedules.json'.format(period=self.period)

    def output(self):
        return {
            'trans_schedule_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/trans_schedules.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'trans-schedule-json', 'from': 'trans_schedules.json',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/trans_schedules.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.106.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateSkyDome(QueenbeeTask):
    """Create a skydome for daylight coefficient studies."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    sky_density = luigi.Parameter(default='1')

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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_sky_dome.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky --sky-density {sky_density}'.format(sky_density=self.sky_density)

    def output(self):
        return {
            'sky_dome': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.dome').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-dome', 'from': 'rflux_sky.sky',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.dome').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateViewFactorModifiers(QueenbeeTask):
    """Get a list of modifiers and a corresponding Octree for surface view factors."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def include_sky(self):
        return 'include'

    @property
    def include_ground(self):
        return 'include'

    @property
    def grouped_shades(self):
        return 'grouped'

    @property
    def model(self):
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_view_factor_modifiers.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance view-factor modifiers model.hbjson --{include_sky}-sky --{include_ground}-ground --{grouped_shades}-shades --name scene'.format(grouped_shades=self.grouped_shades, include_sky=self.include_sky, include_ground=self.include_ground)

    def output(self):
        return {
            'modifiers_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.mod').resolve().as_posix()
            ),
            
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'modifiers-file', 'from': 'scene.mod',
                'to': pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'include_sky': self.include_sky,
            'include_ground': self.include_ground,
            'grouped_shades': self.grouped_shades}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateWea(QueenbeeTask):
    """Translate an .epw file to a .wea file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

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
                pathlib.Path(self.execution_folder, 'radiance/shortwave/in.wea').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/in.wea').resolve().as_posix(),
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


class SetModifiersFromConstructions(QueenbeeTask):
    """Assign honeybee Radiance modifiers based on energy construction properties.

    This includes matching properties for reflectance, absorptance and transmission.
    Furthermore, any dynamic window constructions can be translated to dynamic
    Radiance groups and shade transmittance schedules will be translated to
    dynamic shade groups."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def use_visible(self):
        return 'solar'

    @property
    def dynamic_behavior(self):
        return 'static'

    @property
    def exterior_offset(self):
        return '0.02'

    dynamic_shade = luigi.Parameter(default='dynamic')

    @property
    def model(self):
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'set_modifiers_from_constructions.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy edit modifiers-from-constructions model.hbjson --{use_visible} --{dynamic_behavior}-groups --{dynamic_shade}-groups --exterior-offset {exterior_offset} --output-file new_model.hbjson'.format(dynamic_behavior=self.dynamic_behavior, use_visible=self.use_visible, exterior_offset=self.exterior_offset, dynamic_shade=self.dynamic_shade)

    def output(self):
        return {
            'new_model': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/model.hbjson').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'new-model', 'from': 'new_model.hbjson',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/model.hbjson').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'use_visible': self.use_visible,
            'dynamic_behavior': self.dynamic_behavior,
            'exterior_offset': self.exterior_offset,
            'dynamic_shade': self.dynamic_shade}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/lbt-honeybee:0.8.5'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateDirectSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'sun-only'

    @property
    def output_type(self):
        return 'solar'

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    output_format = luigi.Parameter(default='ASCII')

    sky_density = luigi.Parameter(default='1')

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_direct_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky mtx sky.epw --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(cumulative=self.cumulative, output_type=self.output_type, sky_type=self.sky_type, north=self.north, sun_up_hours=self.sun_up_hours, sky_density=self.sky_density, output_format=self.output_format)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky_direct.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.epw', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky_direct.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'sky_type': self.sky_type,
            'output_type': self.output_type,
            'sun_up_hours': self.sun_up_hours,
            'cumulative': self.cumulative,
            'output_format': self.output_format,
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    grid_filter = luigi.Parameter(default='*')

    @property
    def input_model(self):
        value = pathlib.Path(self.input()['SetModifiersFromConstructions']['new_model'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_rad_folder.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid " {grid_filter} " --grid-check'.format(grid_filter=self.grid_filter)

    def requires(self):
        return {'SetModifiersFromConstructions': SetModifiersFromConstructions(_input_params=self._input_params)}

    def output(self):
        return {
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/model').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature/grids_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/model').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/temperature/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'grid_filter': self.grid_filter}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateTotalSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'total'

    @property
    def output_type(self):
        return 'solar'

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    output_format = luigi.Parameter(default='ASCII')

    sky_density = luigi.Parameter(default='1')

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_total_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky mtx sky.epw --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(cumulative=self.cumulative, output_type=self.output_type, sky_type=self.sky_type, north=self.north, sun_up_hours=self.sun_up_hours, sky_density=self.sky_density, output_format=self.output_format)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.epw', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'sky_type': self.sky_type,
            'output_type': self.output_type,
            'sun_up_hours': self.sun_up_hours,
            'cumulative': self.cumulative,
            'output_format': self.output_format,
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def output_type(self):
        return '1'

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'generate_sunpath.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(north=self.north, output_type=self.output_type)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sunpath': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sunpath.mtx').resolve().as_posix()
            ),
            
            'sun_modifiers': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/suns.mod').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sunpath', 'from': 'sunpath.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sunpath.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/suns.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'output_type': self.output_type}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to multiple destinations."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_grid_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst_1': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition/grids_info.json').resolve().as_posix()
            ),
            
            'dst_2': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity/grids_info.json').resolve().as_posix()
            ),
            
            'dst_3': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_4': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_5': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_6': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/grids_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst-1', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'results/condition/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-2', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-3', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-4', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-5', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-6', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/python:3.7-slim'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateDynamicShadeOctrees(QueenbeeTask):
    """Generate a set of octrees from a folder containing shade transmittance groups."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sunpath(self):
        try:
            pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_dynamic_shade_octrees.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-shade-trans-groups model --sun-path sunpath.mtx --output-folder octree'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_shades').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sunpath', 'to': 'sunpath.mtx', 'from': self.sunpath, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-folder', 'from': 'octree',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_shades').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_octree.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out}'.format(black_out=self.black_out, include_aperture=self.include_aperture)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'black_out': self.black_out,
            'include_aperture': self.include_aperture}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateOctreeWithSuns(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_octree_with_suns.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(black_out=self.black_out, include_aperture=self.include_aperture)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene_with_suns.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene_with_suns.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'black_out': self.black_out,
            'include_aperture': self.include_aperture}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'parse_sun_up_hours.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sun-up-hours.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sun-up-hours.txt').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class SplitAirSpeedFolder(QueenbeeTask):
    """Split an optional folder of data using the same logic as SplitGridFolder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def cpus_per_grid(self):
        return '3'

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def extension(self):
        return '.csv'

    @property
    def input_folder(self):
        try:
            pathlib.Path(self._input_params['air_speed_matrices'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['air_speed_matrices'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid_info_file(self):
        try:
            pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'split_air_speed_folder.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder {cpu_count} {extension} --grid-divisor {cpus_per_grid} --min-sensor-count {min_sensor_count} --grid-info-file grid_info.json'.format(cpus_per_grid=self.cpus_per_grid, extension=self.extension, min_sensor_count=self.min_sensor_count, cpu_count=self.cpu_count)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/air_speeds').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': True},
            {'name': 'grid_info_file', 'to': 'grid_info.json', 'from': self.grid_info_file, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/air_speeds').resolve().as_posix(),
                'optional': True,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'cpu_count': self.cpu_count,
            'cpus_per_grid': self.cpus_per_grid,
            'min_sensor_count': self.min_sensor_count,
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class SplitGridFolder(QueenbeeTask):
    """Create new sensor grids folder with evenly distributed sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def cpus_per_grid(self):
        return '3'

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def input_folder(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'split_grid_folder.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder {cpu_count} --grid-divisor {cpus_per_grid} --min-sensor-count {min_sensor_count}'.format(cpus_per_grid=self.cpus_per_grid, min_sensor_count=self.min_sensor_count, cpu_count=self.cpu_count)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix()
            ),
            
            'dist_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/temperature/_redist_info.json').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/grid/_split_info.json').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dist-info', 'from': 'output_folder/_redist_info.json',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/temperature/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'output_folder/_info.json',
                'to': pathlib.Path(self.execution_folder, 'radiance/grid/_split_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'cpu_count': self.cpu_count,
            'cpus_per_grid': self.cpus_per_grid,
            'min_sensor_count': self.min_sensor_count}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyRedistInfo(QueenbeeTask):
    """Copy a file or folder to multiple destinations."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['dist_info'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_redist_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst_1': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/condition/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_2': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/condition_intensity/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_3': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/TCP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_4': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/HSP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_5': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/CSP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_6': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/_redist_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst-1', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/condition/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-2', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/condition_intensity/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-3', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/TCP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-4', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/HSP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-5', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/CSP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-6', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/python:3.7-slim'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _PrepareFolder_1f915e33Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateModelOccSchedules(_input_params=self.input_values), CreateModelTransSchedules(_input_params=self.input_values), CreateSkyDome(_input_params=self.input_values), CreateViewFactorModifiers(_input_params=self.input_values), CreateDirectSky(_input_params=self.input_values), CreateTotalSky(_input_params=self.input_values), CopyGridInfo(_input_params=self.input_values), CreateDynamicShadeOctrees(_input_params=self.input_values), CreateOctree(_input_params=self.input_values), CreateOctreeWithSuns(_input_params=self.input_values), ParseSunUpHours(_input_params=self.input_values), SplitAirSpeedFolder(_input_params=self.input_values), CopyRedistInfo(_input_params=self.input_values)]
