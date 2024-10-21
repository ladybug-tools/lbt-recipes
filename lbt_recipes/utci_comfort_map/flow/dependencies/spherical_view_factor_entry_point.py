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
from .dependencies.spherical_view_factor import _SphericalViewFactor_1f915e33Orchestrator as SphericalViewFactor_1f915e33Workerbee


_default_inputs = {   'grid_name': None,
    'octree_file_view_factor': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'sensor_count': None,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None,
    'sky_matrix_direct': None,
    'sun_modifiers': None,
    'view_factor_modifiers': None}


class SplitModifiers(QueenbeeTask):
    """Split a single sensor grid file into multiple smaller grids."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def max_value(self):
        return '200000000'

    @property
    def sensor_multiplier(self):
        return '6'

    sensor_count = luigi.Parameter(default='5000')

    @property
    def modifier_file(self):
        value = pathlib.Path(self._input_params['view_factor_modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid_file(self):
        try:
            pathlib.Path(self._input_params['sensor_grid'])
        except TypeError:
            # optional artifact
            return None
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'split_modifiers.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance modifier split-modifiers scene.mod ./output_folder --sensor-count {sensor_count} --grid-file grid.pts --max-value {max_value} --sensor-multiplier {sensor_multiplier}'.format(max_value=self.max_value, sensor_multiplier=self.sensor_multiplier, sensor_count=self.sensor_count)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'split_modifiers').resolve().as_posix()
            ),
            'modifiers': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output_folder/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifier_file', 'to': 'scene.mod', 'from': self.modifier_file, 'optional': False},
            {'name': 'grid_file', 'to': 'grid.pts', 'from': self.grid_file, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'split_modifiers').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'max_value': self.max_value,
            'sensor_multiplier': self.sensor_multiplier,
            'sensor_count': self.sensor_count}

    @property
    def output_parameters(self):
        return [{'name': 'modifiers', 'from': 'output_folder/_info.json', 'to': pathlib.Path(self.params_folder, 'output_folder/_info.json').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.106'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CalculateSphericalViewFactorsLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_name(self):
        return self.item['identifier']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def modifiers(self):
        value = pathlib.Path(self.input()['SplitModifiers']['output_folder'].path, '{item_identifier}.mod'.format(item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file_view_factor'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

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
            'grid_name': self.grid_name,
            'radiance_parameters': self.radiance_parameters,
            'modifiers': self.modifiers,
            'sensor_grid': self.sensor_grid,
            'scene_file': self.scene_file
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [SphericalViewFactor_1f915e33Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'calculate_spherical_view_factors.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'SplitModifiers': SplitModifiers(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'calculate_spherical_view_factors.done').resolve().as_posix())
        }


class CalculateSphericalViewFactors(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def modifiers(self):
        value = pathlib.Path(self.input()['SplitModifiers']['modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.modifiers)
        except:
            # it is a parameter
            return self.input()['SplitModifiers']['modifiers'].path

    def run(self):
        yield [CalculateSphericalViewFactorsLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'calculate_spherical_view_factors.done')
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
        return {'SplitModifiers': SplitModifiers(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'calculate_spherical_view_factors.done').resolve().as_posix())
        }


class RestructureViewFactor(QueenbeeTask):
    """Merge files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return 'npy'

    @property
    def merge_axis(self):
        return '1'

    as_text = luigi.Parameter(default='False')

    delimiter = luigi.Parameter(default='tab')

    fmt = luigi.Parameter(default='%.2f')

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def dist_info(self):
        try:
            pathlib.Path(self.input()['SplitModifiers']['output_folder'].path, '_redist_info.json')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['SplitModifiers']['output_folder'].path, '_redist_info.json')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_view_factor.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess merge merge-files ./input_folder {extension} --output-file output --dist-info dist_info.json --merge-axis "{merge_axis}" --as-text {as_text} --fmt {fmt} --delimiter {delimiter}'.format(fmt=self.fmt, as_text=self.as_text, extension=self.extension, delimiter=self.delimiter, merge_axis=self.merge_axis)

    def requires(self):
        return {'CalculateSphericalViewFactors': CalculateSphericalViewFactors(_input_params=self._input_params), 'SplitModifiers': SplitModifiers(_input_params=self._input_params)}

    def output(self):
        return {
            'output_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../../longwave/view_factors/{name}.npy'.format(name=self.name)).resolve().as_posix()
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
                'name': 'output-file', 'from': 'output.npy',
                'to': pathlib.Path(self.execution_folder, '../../longwave/view_factors/{name}.npy'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'name': self.name,
            'extension': self.extension,
            'merge_axis': self.merge_axis,
            'as_text': self.as_text,
            'delimiter': self.delimiter,
            'fmt': self.fmt}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.443'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _SphericalViewFactorEntryPoint_1f915e33Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [RestructureViewFactor(_input_params=self.input_values)]
