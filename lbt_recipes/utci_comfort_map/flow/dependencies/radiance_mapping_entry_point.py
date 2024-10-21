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


_default_inputs = {   'grid_name': None,
    'model': None,
    'octree_file': None,
    'octree_file_with_suns': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'sensor_count': None,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None,
    'sky_matrix_direct': None,
    'sun_modifiers': None}


class GetEnclosureInfo(QueenbeeTask):
    """Get a JSON of radiant enclosure information from a .pts file of a sensor grid.

    This enclosure info is intended to be consumed by thermal mapping functions."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    air_boundary_distance = luigi.Parameter(default='2m')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def input_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'get_enclosure_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid enclosure-info model.hbjson grid.pts --air-boundary-distance {air_boundary_distance} --output-file enclosure.json'.format(air_boundary_distance=self.air_boundary_distance)

    def output(self):
        return {
            'enclosure_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'enclosures/{name}.json'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False},
            {'name': 'input_grid', 'to': 'grid.pts', 'from': self.input_grid, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'enclosure-file', 'from': 'enclosure.json',
                'to': pathlib.Path(self.execution_folder, 'enclosures/{name}.json'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'air_boundary_distance': self.air_boundary_distance}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class MirrorTheGrid(QueenbeeTask):
    """Split a single sensor grid file into multiple smaller grids."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def vector(self):
        return '0 0 1'

    @property
    def input_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'mirror_the_grid.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid mirror grid.pts --vector "{vector}" --name result --suffix ref'.format(vector=self.vector)

    def output(self):
        return {
            'base_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/grids/{name}.pts'.format(name=self.name)).resolve().as_posix()
            ),
            
            'mirrored_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/grids/{name}_ref.pts'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_grid', 'to': 'grid.pts', 'from': self.input_grid, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'base-file', 'from': 'result.pts',
                'to': pathlib.Path(self.execution_folder, 'shortwave/grids/{name}.pts'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'mirrored-file', 'from': 'result_ref.pts',
                'to': pathlib.Path(self.execution_folder, 'shortwave/grids/{name}_ref.pts'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'vector': self.vector}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class DirectSky(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -ab 1 -c 1 -faf'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    header = luigi.Parameter(default='keep')

    order_by = luigi.Parameter(default='sensor')

    output_format = luigi.Parameter(default='f')

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['sky_matrix_direct'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['MirrorTheGrid']['base_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'direct_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by} --{header}-header'.format(header=self.header, conversion=self.conversion, fixed_radiance_parameters=self.fixed_radiance_parameters, order_by=self.order_by, radiance_parameters=self.radiance_parameters, output_format=self.output_format, sensor_count=self.sensor_count)

    def requires(self):
        return {'MirrorTheGrid': MirrorTheGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/initial_results/direct_sky/{name}.ill'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, 'shortwave/initial_results/direct_sky/{name}.ill'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'radiance_parameters': self.radiance_parameters,
            'fixed_radiance_parameters': self.fixed_radiance_parameters,
            'sensor_count': self.sensor_count,
            'conversion': self.conversion,
            'header': self.header,
            'order_by': self.order_by,
            'output_format': self.output_format}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class DirectSun(QueenbeeTask):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers
    using rcontrib command."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def output_format(self):
        return 'f'

    @property
    def header(self):
        return 'keep'

    calculate_values = luigi.Parameter(default='value')

    order_by = luigi.Parameter(default='sensor')

    @property
    def modifiers(self):
        value = pathlib.Path(self._input_params['sun_modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['MirrorTheGrid']['base_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file_with_suns'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'direct_sun.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance dc scontrib scene.oct grid.pts suns.mod --{calculate_values} --sensor-count {sensor_count} --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --output results.ill --order-by-{order_by} --{header}-header'.format(calculate_values=self.calculate_values, header=self.header, conversion=self.conversion, fixed_radiance_parameters=self.fixed_radiance_parameters, order_by=self.order_by, radiance_parameters=self.radiance_parameters, output_format=self.output_format, sensor_count=self.sensor_count)

    def requires(self):
        return {'MirrorTheGrid': MirrorTheGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/results/direct/{name}.ill'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifiers', 'to': 'suns.mod', 'from': self.modifiers, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, 'shortwave/results/direct/{name}.ill'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'radiance_parameters': self.radiance_parameters,
            'fixed_radiance_parameters': self.fixed_radiance_parameters,
            'sensor_count': self.sensor_count,
            'conversion': self.conversion,
            'output_format': self.output_format,
            'header': self.header,
            'calculate_values': self.calculate_values,
            'order_by': self.order_by}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class GroundReflectedSky(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def output_format(self):
        return 'f'

    @property
    def header(self):
        return 'keep'

    order_by = luigi.Parameter(default='sensor')

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['MirrorTheGrid']['mirrored_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'ground_reflected_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by} --{header}-header'.format(header=self.header, conversion=self.conversion, fixed_radiance_parameters=self.fixed_radiance_parameters, order_by=self.order_by, radiance_parameters=self.radiance_parameters, output_format=self.output_format, sensor_count=self.sensor_count)

    def requires(self):
        return {'MirrorTheGrid': MirrorTheGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/results/reflected/{name}.ill'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, 'shortwave/results/reflected/{name}.ill'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'radiance_parameters': self.radiance_parameters,
            'fixed_radiance_parameters': self.fixed_radiance_parameters,
            'sensor_count': self.sensor_count,
            'conversion': self.conversion,
            'output_format': self.output_format,
            'header': self.header,
            'order_by': self.order_by}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class TotalSky(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1 -faf'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    header = luigi.Parameter(default='keep')

    order_by = luigi.Parameter(default='sensor')

    output_format = luigi.Parameter(default='f')

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['MirrorTheGrid']['base_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'total_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by} --{header}-header'.format(header=self.header, conversion=self.conversion, fixed_radiance_parameters=self.fixed_radiance_parameters, order_by=self.order_by, radiance_parameters=self.radiance_parameters, output_format=self.output_format, sensor_count=self.sensor_count)

    def requires(self):
        return {'MirrorTheGrid': MirrorTheGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/initial_results/total_sky/{name}.ill'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, 'shortwave/initial_results/total_sky/{name}.ill'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'radiance_parameters': self.radiance_parameters,
            'fixed_radiance_parameters': self.fixed_radiance_parameters,
            'sensor_count': self.sensor_count,
            'conversion': self.conversion,
            'header': self.header,
            'order_by': self.order_by,
            'output_format': self.output_format}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class OutputMatrixMath(QueenbeeTask):
    """Subtract direct sky from total sky to get indirect sky."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def output_format(self):
        return 'f'

    @property
    def header(self):
        return 'keep'

    conversion = luigi.Parameter(default=' ')

    @property
    def total_sky_matrix(self):
        value = pathlib.Path(self.input()['TotalSky']['result_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_sky_matrix(self):
        value = pathlib.Path(self.input()['DirectSky']['result_file'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'output_matrix_math.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance mtxop operate-two sky.ill sky_dir.ill --operator "-" --{header}-header --conversion "{conversion}" --output-mtx final.ill --output-format {output_format}'.format(header=self.header, output_format=self.output_format, conversion=self.conversion)

    def requires(self):
        return {'TotalSky': TotalSky(_input_params=self._input_params), 'DirectSky': DirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'shortwave/results/indirect/{name}.ill'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'total_sky_matrix', 'to': 'sky.ill', 'from': self.total_sky_matrix, 'optional': False},
            {'name': 'direct_sky_matrix', 'to': 'sky_dir.ill', 'from': self.direct_sky_matrix, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'final.ill',
                'to': pathlib.Path(self.execution_folder, 'shortwave/results/indirect/{name}.ill'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'output_format': self.output_format,
            'header': self.header,
            'conversion': self.conversion}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _RadianceMappingEntryPoint_1f915e33Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [GetEnclosureInfo(_input_params=self.input_values), DirectSun(_input_params=self.input_values), GroundReflectedSky(_input_params=self.input_values), OutputMatrixMath(_input_params=self.input_values)]
