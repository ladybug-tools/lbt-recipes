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
from queenbee_local import load_input_param as qb_load_input_param
from .dependencies.annual_daylight_ray_tracing import _AnnualDaylightRayTracing_8529a1a1Orchestrator as AnnualDaylightRayTracing_8529a1a1Workerbee


_default_inputs = {   'bsdf_folder': None,
    'direct_sky': None,
    'identifier': '__static__',
    'light_path': '__static__',
    'octree_file': None,
    'octree_file_direct': None,
    'octree_file_with_suns': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'results_folder': 'results',
    'sensor_grids_folder': None,
    'sensor_grids_info': [],
    'simulation_folder': '.',
    'sky_dome': None,
    'sun_modifiers': None,
    'total_sky': None}


class RestructureDirectSunlightResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def identifier(self):
        return self._input_params['identifier']

    @property
    def light_path(self):
        return self._input_params['light_path']

    @property
    def extension(self):
        return 'ill'

    @property
    def results_folder(self):
        return self._input_params['results_folder']

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/final/direct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dist_info(self):
        try:
            pathlib.Path(self._input_params['sensor_grids_folder'], '_redist_info.json')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['sensor_grids_folder'], '_redist_info.json')
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
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'TwoPhaseRaytracing': TwoPhaseRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{results_folder}/{light_path}/{identifier}/direct'.format(results_folder=self.results_folder, light_path=self.light_path, identifier=self.identifier)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False},
            {'name': 'dist_info', 'to': 'dist_info.json', 'from': self.dist_info, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, '{results_folder}/{light_path}/{identifier}/direct'.format(results_folder=self.results_folder, light_path=self.light_path, identifier=self.identifier)).resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class RestructureTotalResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def identifier(self):
        return self._input_params['identifier']

    @property
    def light_path(self):
        return self._input_params['light_path']

    @property
    def extension(self):
        return 'ill'

    @property
    def results_folder(self):
        return self._input_params['results_folder']

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/final/total')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dist_info(self):
        try:
            pathlib.Path(self._input_params['sensor_grids_folder'], '_redist_info.json')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['sensor_grids_folder'], '_redist_info.json')
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
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'TwoPhaseRaytracing': TwoPhaseRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{results_folder}/{light_path}/{identifier}/total'.format(results_folder=self.results_folder, light_path=self.light_path, identifier=self.identifier)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False},
            {'name': 'dist_info', 'to': 'dist_info.json', 'from': self.dist_info, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, '{results_folder}/{light_path}/{identifier}/total'.format(results_folder=self.results_folder, light_path=self.light_path, identifier=self.identifier)).resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class TwoPhaseRaytracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def octree_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_direct(self):
        value = pathlib.Path(self._input_params['octree_file_direct'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self._input_params['octree_file_with_suns'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grids_folder'], '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['total_sky'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self._input_params['direct_sky'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self._input_params['sun_modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self._input_params['bsdf_folder'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['bsdf_folder'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_full_id}'.format(item_full_id=self.item['full_id'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'octree_file_direct': self.octree_file_direct,
            'octree_file_with_suns': self.octree_file_with_suns,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sky_dome': self.sky_dome,
            'sun_modifiers': self.sun_modifiers,
            'bsdfs': self.bsdfs
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [AnnualDaylightRayTracing_8529a1a1Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'two_phase_raytracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'two_phase_raytracing.done').resolve().as_posix())
        }


class TwoPhaseRaytracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids_info(self):
        value = pathlib.Path(self._input_params['sensor_grids_info'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids_info)
        except:
            # it is a parameter
            return self._input_params['sensor_grids_info']

    def run(self):
        yield [TwoPhaseRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'two_phase_raytracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()


    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'two_phase_raytracing.done').resolve().as_posix())
        }


class _TwoPhase_8529a1a1Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [RestructureDirectSunlightResults(_input_params=self.input_values), RestructureTotalResults(_input_params=self.input_values)]
