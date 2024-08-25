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
from .dependencies.energy_simulation import _EnergySimulation_73edd45fOrchestrator as EnergySimulation_73edd45fWorkerbee
from .dependencies.prepare_folder import _PrepareFolder_73edd45fOrchestrator as PrepareFolder_73edd45fWorkerbee
from .dependencies.comfort_mapping_entry_point import _ComfortMappingEntryPoint_73edd45fOrchestrator as ComfortMappingEntryPoint_73edd45fWorkerbee
from .dependencies.dynamic_contribution_entry_point import _DynamicContributionEntryPoint_73edd45fOrchestrator as DynamicContributionEntryPoint_73edd45fWorkerbee
from .dependencies.dynamic_shade_contrib_entry_point import _DynamicShadeContribEntryPoint_73edd45fOrchestrator as DynamicShadeContribEntryPoint_73edd45fWorkerbee
from .dependencies.radiance_mapping_entry_point import _RadianceMappingEntryPoint_73edd45fOrchestrator as RadianceMappingEntryPoint_73edd45fWorkerbee
from .dependencies.spherical_view_factor_entry_point import _SphericalViewFactorEntryPoint_73edd45fOrchestrator as SphericalViewFactorEntryPoint_73edd45fWorkerbee


_default_inputs = {   'additional_idf': None,
    'air_speed': None,
    'clo_value': None,
    'comfort_parameters': '--ppd-threshold 10',
    'cpu_count': 50,
    'ddy': None,
    'epw': None,
    'met_rate': None,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'run_period': '',
    'simulation_folder': '.',
    'solarcal_parameters': '--posture seated --sharp 135 --absorptivity 0.7 '
                           '--emissivity 0.95',
    'write_set_map': 'write-op-map'}


class CreateResultInfo(QueenbeeTask):
    """Get a JSON that specifies the data type and units for comfort map outputs."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def comfort_model(self):
        return 'pmv'

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def qualifier(self):
        return self._input_params['write_set_map']

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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_result_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'ladybug-comfort map map-result-info {comfort_model} --run-period "{run_period}" --qualifier "{qualifier}" --folder output --log-file results_info.json'.format(comfort_model=self.comfort_model, qualifier=self.qualifier, run_period=self.run_period)

    def output(self):
        return {
            'temperature_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature/results_info.json').resolve().as_posix()
            ),
            
            'condition_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition/results_info.json').resolve().as_posix()
            ),
            
            'condition_intensity_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity/results_info.json').resolve().as_posix()
            ),
            
            'tcp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP/vis_metadata.json').resolve().as_posix()
            ),
            
            'hsp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP/vis_metadata.json').resolve().as_posix()
            ),
            
            'csp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP/vis_metadata.json').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'temperature-info', 'from': 'output/temperature.json',
                'to': pathlib.Path(self.execution_folder, 'results/temperature/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'condition-info', 'from': 'output/condition.json',
                'to': pathlib.Path(self.execution_folder, 'results/condition/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'condition-intensity-info', 'from': 'output/condition_intensity.json',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'tcp-vis-metadata', 'from': 'output/TCP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'hsp-vis-metadata', 'from': 'output/HSP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'csp-vis-metadata', 'from': 'output/CSP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'comfort_model': self.comfort_model,
            'run_period': self.run_period,
            'qualifier': self.qualifier}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/ladybug-comfort:0.18.42'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class EnergySimulation(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def run_period(self):
        return self._input_params['run_period']

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

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'model': self.model,
            'epw': self.epw,
            'ddy': self.ddy,
            'north': self.north,
            'run_period': self.run_period,
            'additional_idf': self.additional_idf
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [EnergySimulation_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'energy_simulation.done').write_text('done!')

    def output(self):
        return {
            'energy': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'energy_simulation.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'energy', 'from': 'energy',
                'to': pathlib.Path(self.execution_folder, 'energy').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class PrepareFolder(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

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
            'model': self.model,
            'epw': self.epw,
            'north': self.north,
            'run_period': self.run_period,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [PrepareFolder_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder.done').write_text('done!')

    def output(self):
        return {
            
            'results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            ),
            
            'initial_results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix()
            ),
            
            'metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            ),
            
            'sensor_grids_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix()
            ),
            
            'shortwave_resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources').resolve().as_posix()
            ),
            
            'longwave_resources': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/longwave/resources').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'radiance/grid/_split_info.json').resolve().as_posix()
                ),
                'dynamic_abtracted_octrees': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'radiance/shortwave/resources/dynamic_groups/group_info.json').resolve().as_posix()
                ),
                'dynamic_shade_octrees': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'radiance/shortwave/resources/dynamic_shades/trans_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results', 'from': 'results',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'initial-results', 'from': 'initial_results',
                'to': pathlib.Path(self.execution_folder, 'initial_results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'sensor-grids-folder', 'from': 'radiance/grid',
                'to': pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'shortwave-resources', 'from': 'radiance/shortwave/resources',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'longwave-resources', 'from': 'radiance/longwave/resources',
                'to': pathlib.Path(self.execution_folder, 'radiance/longwave/resources').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'radiance/grid/_split_info.json', 'to': pathlib.Path(self.params_folder, 'radiance/grid/_split_info.json').resolve().as_posix()},
                {'name': 'dynamic-abtracted-octrees', 'from': 'radiance/shortwave/resources/dynamic_groups/group_info.json', 'to': pathlib.Path(self.params_folder, 'radiance/shortwave/resources/dynamic_groups/group_info.json').resolve().as_posix()},
                {'name': 'dynamic-shade-octrees', 'from': 'radiance/shortwave/resources/dynamic_shades/trans_info.json', 'to': pathlib.Path(self.params_folder, 'radiance/shortwave/resources/dynamic_shades/trans_info.json').resolve().as_posix()}]


class CopyResultInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateResultInfo']['temperature_info'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_result_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateResultInfo': CreateResultInfo(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/results_info.json').resolve().as_posix()
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
                'name': 'dst', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/results_info.json').resolve().as_posix(),
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


class RunRadianceSimulationLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

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
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'scene_with_suns.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sensor_grids_folder'].path, '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky_direct.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'suns.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

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
            'model': self.model,
            'octree_file_with_suns': self.octree_file_with_suns,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [RadianceMappingEntryPoint_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_simulation.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_simulation.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'enclosures', 'from': 'enclosures',
                'to': pathlib.Path(self.execution_folder, 'radiance/enclosures').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'shortwave-results', 'from': 'shortwave/results',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'shortwave-grids', 'from': 'shortwave/grids',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/grids').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class RunRadianceSimulation(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['sensor_grids'].path

    def run(self):
        yield [RunRadianceSimulationLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_simulation.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_simulation.done').resolve().as_posix())
        }


class RunSphericalViewFactorSimulationLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def octree_file_view_factor(self):
        value = pathlib.Path(self.input()['PrepareFolder']['longwave_resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sensor_grids_folder'].path, '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_factor_modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolder']['longwave_resources'].path, 'scene.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance/view_factor/{item_full_id}'.format(item_full_id=self.item['full_id'])).resolve().as_posix()

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
            'octree_file_view_factor': self.octree_file_view_factor,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'view_factor_modifiers': self.view_factor_modifiers
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [SphericalViewFactorEntryPoint_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_spherical_view_factor_simulation.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_spherical_view_factor_simulation.done').resolve().as_posix())
        }


class RunSphericalViewFactorSimulation(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['sensor_grids'].path

    def run(self):
        yield [RunSphericalViewFactorSimulationLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_spherical_view_factor_simulation.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_spherical_view_factor_simulation.done').resolve().as_posix())
        }


class RunRadianceDynamicContributionLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def group_name(self):
        return self.item['identifier']

    @property
    def sensor_grids(self):
        return qb_load_input_param(
                self.input()['PrepareFolder']['sensor_grids'].path
            )

    @property
    def result_sql(self):
        value = pathlib.Path(self.input()['EnergySimulation']['energy'].path, 'eplusout.sql')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_spec(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'dynamic_groups/{item_identifier}/{item_spec}'.format(item_spec=self.item['spec'], item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_diff(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'dynamic_groups/{item_identifier}/{item_diff}'.format(item_diff=self.item['diff'], item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'dynamic_groups/{item_identifier}/{item_sun}'.format(item_sun=self.item['sun'], item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid_folder(self):
        value = pathlib.Path('radiance/shortwave/grids')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky_direct.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'suns.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sun-up-hours.txt')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

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
            'result_sql': self.result_sql,
            'octree_file_spec': self.octree_file_spec,
            'octree_file_diff': self.octree_file_diff,
            'octree_file_with_suns': self.octree_file_with_suns,
            'group_name': self.group_name,
            'sensor_grid_folder': self.sensor_grid_folder,
            'sensor_grids': self.sensor_grids,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'sun_up_hours': self.sun_up_hours
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DynamicContributionEntryPoint_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'EnergySimulation': EnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done').resolve().as_posix())
        }


class RunRadianceDynamicContribution(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def dynamic_abtracted_octrees(self):
        value = pathlib.Path(self.input()['PrepareFolder']['dynamic_abtracted_octrees'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.dynamic_abtracted_octrees)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['dynamic_abtracted_octrees'].path

    def run(self):
        yield [RunRadianceDynamicContributionLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'EnergySimulation': EnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done').resolve().as_posix())
        }


class RunRadianceShadeContributionLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def group_name(self):
        return self.item['identifier']

    @property
    def sensor_grids(self):
        return qb_load_input_param(
                self.input()['PrepareFolder']['sensor_grids'].path
            )

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'dynamic_shades/{item_default}'.format(item_default=self.item['default']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'dynamic_shades/{item_sun}'.format(item_sun=self.item['sun']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid_folder(self):
        value = pathlib.Path('radiance/shortwave/grids')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.dome')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sky_direct.mtx')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'suns.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sun-up-hours.txt')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

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
            'octree_file_with_suns': self.octree_file_with_suns,
            'group_name': self.group_name,
            'sensor_grid_folder': self.sensor_grid_folder,
            'sensor_grids': self.sensor_grids,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'sun_up_hours': self.sun_up_hours
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DynamicShadeContribEntryPoint_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done').resolve().as_posix())
        }


class RunRadianceShadeContribution(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def dynamic_shade_octrees(self):
        value = pathlib.Path(self.input()['PrepareFolder']['dynamic_shade_octrees'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.dynamic_shade_octrees)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['dynamic_shade_octrees'].path

    def run(self):
        yield [RunRadianceShadeContributionLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done').resolve().as_posix())
        }


class RunComfortMapLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def solarcal_par(self):
        return self._input_params['solarcal_parameters']

    @property
    def comfort_parameters(self):
        return self._input_params['comfort_parameters']

    @property
    def write_set_map(self):
        return self._input_params['write_set_map']

    solarcal_parameters = luigi.Parameter(default='--posture seated --sharp 135 --absorptivity 0.7 --emissivity 0.95')

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def result_sql(self):
        value = pathlib.Path(self.input()['EnergySimulation']['energy'].path, 'eplusout.sql')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path('radiance/enclosures', '{item_full_id}.json'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_factors(self):
        value = pathlib.Path('radiance/longwave/view_factors', '{item_full_id}.npy'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def modifiers(self):
        value = pathlib.Path(self.input()['PrepareFolder']['longwave_resources'].path, 'scene.mod')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def indirect_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/indirect', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/direct', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/reflected', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'sun-up-hours.txt')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def contributions(self):
        try:
            pathlib.Path('radiance/shortwave/dynamic/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('radiance/shortwave/dynamic/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def transmittance_contribs(self):
        try:
            pathlib.Path('radiance/shortwave/shd_trans/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('radiance/shortwave/shd_trans/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def trans_schedules(self):
        value = pathlib.Path(self.input()['PrepareFolder']['shortwave_resources'].path, 'trans_schedules.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def occ_schedules(self):
        value = pathlib.Path(self.input()['PrepareFolder']['metrics'].path, 'occupancy_schedules.json')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def air_speed(self):
        try:
            pathlib.Path(self._input_params['air_speed'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['air_speed'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def met_rate(self):
        try:
            pathlib.Path(self._input_params['met_rate'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['met_rate'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def clo_value(self):
        try:
            pathlib.Path(self._input_params['clo_value'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['clo_value'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results').resolve().as_posix()

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
            'epw': self.epw,
            'result_sql': self.result_sql,
            'grid_name': self.grid_name,
            'enclosure_info': self.enclosure_info,
            'view_factors': self.view_factors,
            'modifiers': self.modifiers,
            'indirect_irradiance': self.indirect_irradiance,
            'direct_irradiance': self.direct_irradiance,
            'ref_irradiance': self.ref_irradiance,
            'sun_up_hours': self.sun_up_hours,
            'contributions': self.contributions,
            'transmittance_contribs': self.transmittance_contribs,
            'trans_schedules': self.trans_schedules,
            'occ_schedules': self.occ_schedules,
            'run_period': self.run_period,
            'air_speed': self.air_speed,
            'met_rate': self.met_rate,
            'clo_value': self.clo_value,
            'solarcal_par': self.solarcal_par,
            'comfort_parameters': self.comfort_parameters,
            'write_set_map': self.write_set_map
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [ComfortMappingEntryPoint_73edd45fWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_comfort_map.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'EnergySimulation': EnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params), 'RunRadianceDynamicContribution': RunRadianceDynamicContribution(_input_params=self._input_params), 'RunRadianceShadeContribution': RunRadianceShadeContribution(_input_params=self._input_params), 'RunSphericalViewFactorSimulation': RunSphericalViewFactorSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_comfort_map.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-folder', 'from': 'results',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'conditions', 'from': 'conditions',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class RunComfortMap(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['PrepareFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['PrepareFolder']['sensor_grids'].path

    def run(self):
        yield [RunComfortMapLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_comfort_map.done')
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
        return {'PrepareFolder': PrepareFolder(_input_params=self._input_params), 'EnergySimulation': EnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params), 'RunRadianceDynamicContribution': RunRadianceDynamicContribution(_input_params=self._input_params), 'RunRadianceShadeContribution': RunRadianceShadeContribution(_input_params=self._input_params), 'RunSphericalViewFactorSimulation': RunSphericalViewFactorSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_comfort_map.done').resolve().as_posix())
        }


class RestructureConditionIntensityResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    as_text = luigi.Parameter(default='False')

    delimiter = luigi.Parameter(default='tab')

    fmt = luigi.Parameter(default='%.2f')

    output_extension = luigi.Parameter(default='ill')

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/condition_intensity')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_condition_intensity_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json --output-extension {output_extension} --as-text {as_text} --fmt {fmt} --delimiter {delimiter}'.format(as_text=self.as_text, output_extension=self.output_extension, fmt=self.fmt, extension=self.extension, delimiter=self.delimiter)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension,
            'as_text': self.as_text,
            'delimiter': self.delimiter,
            'fmt': self.fmt,
            'output_extension': self.output_extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.431'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureConditionResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    as_text = luigi.Parameter(default='False')

    delimiter = luigi.Parameter(default='tab')

    fmt = luigi.Parameter(default='%.2f')

    output_extension = luigi.Parameter(default='ill')

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/condition')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_condition_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json --output-extension {output_extension} --as-text {as_text} --fmt {fmt} --delimiter {delimiter}'.format(as_text=self.as_text, output_extension=self.output_extension, fmt=self.fmt, extension=self.extension, delimiter=self.delimiter)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/condition').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension,
            'as_text': self.as_text,
            'delimiter': self.delimiter,
            'fmt': self.fmt,
            'output_extension': self.output_extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.431'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureCspResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/CSP')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_csp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.103'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureHspResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/HSP')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_hsp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.103'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureTcpResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/TCP')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_tcp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.103'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureTemperatureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    as_text = luigi.Parameter(default='False')

    delimiter = luigi.Parameter(default='tab')

    fmt = luigi.Parameter(default='%.2f')

    output_extension = luigi.Parameter(default='ill')

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/temperature')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_temperature_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ./output_folder {extension} --dist-info dist_info.json --output-extension {output_extension} --as-text {as_text} --fmt {fmt} --delimiter {delimiter}'.format(as_text=self.as_text, output_extension=self.output_extension, fmt=self.fmt, extension=self.extension, delimiter=self.delimiter)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/temperature').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension,
            'as_text': self.as_text,
            'delimiter': self.delimiter,
            'fmt': self.fmt,
            'output_extension': self.output_extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.431'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _Main_73edd45fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CopyResultInfo(_input_params=self.input_values), RestructureConditionIntensityResults(_input_params=self.input_values), RestructureConditionResults(_input_params=self.input_values), RestructureCspResults(_input_params=self.input_values), RestructureHspResults(_input_params=self.input_values), RestructureTcpResults(_input_params=self.input_values), RestructureTemperatureResults(_input_params=self.input_values)]
