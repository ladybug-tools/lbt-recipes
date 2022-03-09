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


_default_inputs = {   'aperture_id': None,
    'direct_specular': None,
    'grid_name': None,
    'indirect_diffuse': None,
    'indirect_specular': None,
    'params_folder': '__params',
    'ref_diffuse': None,
    'ref_specular': None,
    'result_sql': None,
    'simulation_folder': '.',
    'sun_up_hours': None}


class CreateIrradianceContribMap(QueenbeeTask):
    """Get .ill files with maps of irradiance contributions from dynamic windows."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def aperture_id(self):
        return self._input_params['aperture_id']

    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def result_sql(self):
        value = pathlib.Path(self._input_params['result_sql'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_specular(self):
        value = pathlib.Path(self._input_params['direct_specular'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def indirect_specular(self):
        value = pathlib.Path(self._input_params['indirect_specular'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_specular(self):
        value = pathlib.Path(self._input_params['ref_specular'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def indirect_diffuse(self):
        value = pathlib.Path(self._input_params['indirect_diffuse'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_diffuse(self):
        value = pathlib.Path(self._input_params['ref_diffuse'])
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
        return 'ladybug-comfort map irradiance-contrib result.sql direct_spec.ill indirect_spec.ill ref_spec.ill indirect_diff.ill ref_diff.ill sun-up-hours.txt --aperture-id "{aperture_id}" --folder output'.format(aperture_id=self.aperture_id)

    def output(self):
        return {
            'result_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'dynamic/final/{name}/{aperture_id}'.format(name=self.name, aperture_id=self.aperture_id)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_sql', 'to': 'result.sql', 'from': self.result_sql, 'optional': False},
            {'name': 'direct_specular', 'to': 'direct_spec.ill', 'from': self.direct_specular, 'optional': False},
            {'name': 'indirect_specular', 'to': 'indirect_spec.ill', 'from': self.indirect_specular, 'optional': False},
            {'name': 'ref_specular', 'to': 'ref_spec.ill', 'from': self.ref_specular, 'optional': False},
            {'name': 'indirect_diffuse', 'to': 'indirect_diff.ill', 'from': self.indirect_diffuse, 'optional': False},
            {'name': 'ref_diffuse', 'to': 'ref_diff.ill', 'from': self.ref_diffuse, 'optional': False},
            {'name': 'sun_up_hours', 'to': 'sun-up-hours.txt', 'from': self.sun_up_hours, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-folder', 'from': 'output',
                'to': pathlib.Path(self.execution_folder, 'dynamic/final/{name}/{aperture_id}'.format(name=self.name, aperture_id=self.aperture_id)).resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _DynamicBehaviorEntryPoint_5e24b5e4Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateIrradianceContribMap(_input_params=self.input_values)]
