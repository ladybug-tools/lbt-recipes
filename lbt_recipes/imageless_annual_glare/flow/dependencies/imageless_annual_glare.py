"""
This file is auto-generated from imageless-annual-glare:0.1.5.
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


_default_inputs = {   'bsdfs': None,
    'grid_name': None,
    'luminance_factor': 2000.0,
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'sensor_count': None,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None}


class DirectSky(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -ab 1 -c 1'

    @property
    def output_format(self):
        return 'f'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    header = luigi.Parameter(default='keep')

    input_format = luigi.Parameter(default='a')

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
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
        return 'honeybee-radiance dc coeff scene.oct grid.pts sky.dome --sensor-count {sensor_count} --output results.mtx --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --input-format {input_format} --output-format {output_format} --{header}-header'.format(fixed_radiance_parameters=self.fixed_radiance_parameters, input_format=self.input_format, header=self.header, sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, output_format=self.output_format)

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'dc_direct.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.mtx',
                'to': pathlib.Path(self.execution_folder, 'dc_direct.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.126'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class TotalSky(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1'

    @property
    def output_format(self):
        return 'f'

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    header = luigi.Parameter(default='keep')

    input_format = luigi.Parameter(default='a')

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
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
        return 'honeybee-radiance dc coeff scene.oct grid.pts sky.dome --sensor-count {sensor_count} --output results.mtx --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --input-format {input_format} --output-format {output_format} --{header}-header'.format(fixed_radiance_parameters=self.fixed_radiance_parameters, input_format=self.input_format, header=self.header, sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, output_format=self.output_format)

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'dc_total.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.mtx',
                'to': pathlib.Path(self.execution_folder, 'dc_total.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.126'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class DaylightGlareProbability(QueenbeeTask):
    """Calculates DGP for all sky conditions in the sky matrix, but filtered by an
    occupancy schedule. This means that unoccupied hours will be zero DGP. If the
    occupancy schedule is not given or does not exists the DGP will be calculated
    for all hours."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def threshold_factor(self):
        return self._input_params['luminance_factor']

    @property
    def dc_direct(self):
        value = pathlib.Path(self.input()['DirectSky']['result_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dc_total(self):
        value = pathlib.Path(self.input()['TotalSky']['result_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_vector(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_rays(self):
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

    def command(self):
        return 'honeybee-radiance dcglare two-phase dc_direct.mtx dc_total.mtx sky.smx view_rays.ray --threshold-factor {threshold_factor} --occupancy-schedule schedule.txt --output view_rays.dgp'.format(threshold_factor=self.threshold_factor)

    def requires(self):
        return {'TotalSky': TotalSky(_input_params=self._input_params), 'DirectSky': DirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'view_rays_dgp': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../dgp/{name}.dgp'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'dc_direct', 'to': 'dc_direct.mtx', 'from': self.dc_direct, 'optional': False},
            {'name': 'dc_total', 'to': 'dc_total.mtx', 'from': self.dc_total, 'optional': False},
            {'name': 'sky_vector', 'to': 'sky.smx', 'from': self.sky_vector, 'optional': False},
            {'name': 'view_rays', 'to': 'view_rays.ray', 'from': self.view_rays, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'view-rays-dgp', 'from': 'view_rays.dgp',
                'to': pathlib.Path(self.execution_folder, '../dgp/{name}.dgp'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.126'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _ImagelessAnnualGlare_810c23b0Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [DaylightGlareProbability(_input_params=self.input_values)]
