"""
This file is auto-generated from annual-daylight-enhanced:0.0.2.
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
from .dependencies.two_phase_simulation import _TwoPhaseSimulation_33a9e3b7Orchestrator as TwoPhaseSimulation_33a9e3b7Workerbee
from .dependencies.two_phase_prepare_folder import _TwoPhasePrepareFolder_33a9e3b7Orchestrator as TwoPhasePrepareFolder_33a9e3b7Workerbee


_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05 -dr 0',
    'simulation_folder': '.',
    'wea': None}


class PrepareFolderAnnualDaylight(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
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
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'north': self.north,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'grid_filter': self.grid_filter,
            'model': self.model,
            'wea': self.wea
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [TwoPhasePrepareFolder_33a9e3b7Workerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder_annual_daylight.done').write_text('done!')

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources').resolve().as_posix()
            ),
            
            'results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            ),
            'two_phase_info': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'resources/two_phase.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder_annual_daylight.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'model').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'resources', 'from': 'resources',
                'to': pathlib.Path(self.execution_folder, 'resources').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'results', 'from': 'results',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'two-phase-info', 'from': 'resources/two_phase.json', 'to': pathlib.Path(self.params_folder, 'resources/two_phase.json').resolve().as_posix()}]


class CalculateTwoPhaseMatrixLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def identifier(self):
        return self.item['identifier']

    @property
    def light_path(self):
        return self.item['light_path']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def sensor_grids_info(self):
        return self.item['sensor_grids_info']

    @property
    def results_folder(self):
        return '../../../results'

    @property
    def sensor_grids_folder(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'dynamic/grid/{item_sensor_grids_folder}'.format(item_sensor_grids_folder=self.item['sensor_grids_folder']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'dynamic/octree/{item_octree}'.format(item_octree=self.item['octree']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_direct(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'dynamic/octree/{item_octree_direct}'.format(item_octree_direct=self.item['octree_direct']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'dynamic/octree/{item_octree_direct_sun}'.format(item_octree_direct_sun=self.item['octree_direct_sun']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def total_sky(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_sky(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'sky_direct.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['resources'].path, 'suns.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['model_folder'].path, 'bsdf')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'calcs/2_phase/{item_identifier}'.format(item_identifier=self.item['identifier'])).resolve().as_posix()

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
            'identifier': self.identifier,
            'light_path': self.light_path,
            'radiance_parameters': self.radiance_parameters,
            'sensor_grids_info': self.sensor_grids_info,
            'sensor_grids_folder': self.sensor_grids_folder,
            'octree_file': self.octree_file,
            'octree_file_direct': self.octree_file_direct,
            'octree_file_with_suns': self.octree_file_with_suns,
            'sky_dome': self.sky_dome,
            'total_sky': self.total_sky,
            'direct_sky': self.direct_sky,
            'sun_modifiers': self.sun_modifiers,
            'bsdf_folder': self.bsdf_folder,
            'results_folder': self.results_folder
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [TwoPhaseSimulation_33a9e3b7Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'calculate_two_phase_matrix.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'calculate_two_phase_matrix.done').resolve().as_posix())
        }


class CalculateTwoPhaseMatrix(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def two_phase_info(self):
        value = pathlib.Path(self.input()['PrepareFolderAnnualDaylight']['two_phase_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.two_phase_info)
        except:
            # it is a parameter
            return self.input()['PrepareFolderAnnualDaylight']['two_phase_info'].path

    def run(self):
        yield [CalculateTwoPhaseMatrixLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'calculate_two_phase_matrix.done')
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

    def requires(self):
        return {'PrepareFolderAnnualDaylight': PrepareFolderAnnualDaylight(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'calculate_two_phase_matrix.done').resolve().as_posix())
        }


class _Main_33a9e3b7Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CalculateTwoPhaseMatrix(_input_params=self.input_values)]
