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


_default_inputs = {   'grid_name': None,
    'modifiers': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'scene_file': None,
    'sensor_grid': None,
    'simulation_folder': '.'}


class ComputeSphericalViewFactors(QueenbeeTask):
    """Calculate spherical view factor contribution for a grid of sensors."""

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

    ray_count = luigi.Parameter(default='6')

    @property
    def modifiers(self):
        value = pathlib.Path(self._input_params['modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['scene_file'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'compute_spherical_view_factors.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess view-factor contrib scene.oct grid.pts scene.mod --ray-count {ray_count} --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --name view_factor'.format(radiance_parameters=self.radiance_parameters, ray_count=self.ray_count, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def output(self):
        return {
            'view_factor_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/{name}.npy'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifiers', 'to': 'scene.mod', 'from': self.modifiers, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'view-factor-file', 'from': 'view_factor.npy',
                'to': pathlib.Path(self.execution_folder, 'initial_results/{name}.npy'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'radiance_parameters': self.radiance_parameters,
            'fixed_radiance_parameters': self.fixed_radiance_parameters,
            'ray_count': self.ray_count}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.431'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _SphericalViewFactor_73edd45fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [ComputeSphericalViewFactors(_input_params=self.input_values)]
