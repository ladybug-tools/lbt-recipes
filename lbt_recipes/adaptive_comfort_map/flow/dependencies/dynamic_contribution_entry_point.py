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
from .dependencies.radiance_contrib_entry_point import _RadianceContribEntryPoint_a0dda991Orchestrator as RadianceContribEntryPoint_a0dda991Workerbee


_default_inputs = {   'group_name': None,
    'octree_file_diff': None,
    'octree_file_spec': None,
    'octree_file_with_suns': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'result_sql': None,
    'sensor_grid_folder': None,
    'sensor_grids': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None,
    'sky_matrix_direct': None,
    'sun_modifiers': None,
    'sun_up_hours': None}


class ReadGrids(QueenbeeTask):
    """Read the content of a JSON file as a list."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['sensor_grids'])
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
        return 'echo parsing JSON information to a list...'

    def output(self):
        return {'data': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'input_path').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_parameters(self):
        return [{'name': 'data', 'from': 'input_path', 'to': pathlib.Path(self.params_folder, 'input_path').resolve().as_posix()}]


class RunRadianceWindowContribLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def group_name(self):
        return self._input_params['group_name']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def octree_file_spec(self):
        value = pathlib.Path(self._input_params['octree_file_spec'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_diff(self):
        value = pathlib.Path(self._input_params['octree_file_diff'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self._input_params['octree_file_with_suns'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid_folder'], '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_sensor_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid_folder'], '{item_full_id}_ref.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self._input_params['sun_modifiers'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def result_sql(self):
        value = pathlib.Path(self._input_params['result_sql'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self._input_params['sun_up_hours'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'shortwave').resolve().as_posix()

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
            'octree_file_spec': self.octree_file_spec,
            'octree_file_diff': self.octree_file_diff,
            'octree_file_with_suns': self.octree_file_with_suns,
            'group_name': self.group_name,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'ref_sensor_grid': self.ref_sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'result_sql': self.result_sql,
            'sun_up_hours': self.sun_up_hours
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [RadianceContribEntryPoint_a0dda991Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_window_contrib.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'ReadGrids': ReadGrids(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_window_contrib.done').resolve().as_posix())
        }


class RunRadianceWindowContrib(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def data(self):
        value = pathlib.Path(self.input()['ReadGrids']['data'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.data)
        except:
            # it is a parameter
            return self.input()['ReadGrids']['data'].path

    def run(self):
        yield [RunRadianceWindowContribLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_window_contrib.done')
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
        return {'ReadGrids': ReadGrids(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_window_contrib.done').resolve().as_posix())
        }


class _DynamicContributionEntryPoint_a0dda991Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [RunRadianceWindowContrib(_input_params=self.input_values)]
