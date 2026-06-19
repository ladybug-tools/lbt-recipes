"""
This file is auto-generated from leed-daylight-option-two:0.3.10.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    pollination: info@pollination.solutions

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_


_default_inputs = {   'illuminance_3pm': None,
    'illuminance_9am': None,
    'model': None,
    'params_folder': '__params',
    'pass_fail_3pm': None,
    'pass_fail_9am': None,
    'pass_fail_combined': None,
    'simulation_folder': '.'}


class CopyIlluminance3pm(QueenbeeTask):
    """Copy a folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['illuminance_3pm'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_illuminance_3pm.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input folder...'

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization/illuminance-3pm').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input.path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input.path',
                'to': pathlib.Path(self.execution_folder, 'visualization/illuminance-3pm').resolve().as_posix(),
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


class CopyIlluminance9am(QueenbeeTask):
    """Copy a folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['illuminance_9am'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_illuminance_9am.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input folder...'

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization/illuminance-9am').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input.path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input.path',
                'to': pathlib.Path(self.execution_folder, 'visualization/illuminance-9am').resolve().as_posix(),
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


class CopyPassFail3pm(QueenbeeTask):
    """Copy a folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['pass_fail_3pm'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_pass_fail_3pm.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input folder...'

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization/pass-fail-3pm').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input.path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input.path',
                'to': pathlib.Path(self.execution_folder, 'visualization/pass-fail-3pm').resolve().as_posix(),
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


class CopyPassFail9am(QueenbeeTask):
    """Copy a folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['pass_fail_9am'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_pass_fail_9am.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input folder...'

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization/pass-fail-9am').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input.path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input.path',
                'to': pathlib.Path(self.execution_folder, 'visualization/pass-fail-9am').resolve().as_posix(),
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


class CopyPassFailCombined(QueenbeeTask):
    """Copy a folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['pass_fail_combined'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_pass_fail_combined.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input folder...'

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization/pass-fail-combined').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input.path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input.path',
                'to': pathlib.Path(self.execution_folder, 'visualization/pass-fail-combined').resolve().as_posix(),
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


class CreateVisMetadata(QueenbeeTask):
    """Create five visualization metadata files for LEED Daylight Option Two."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    output_folder = luigi.Parameter(default='visualization')

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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_vis_metadata.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance post-process leed-daylight-option-two-vis-metadata --output-folder "{output_folder}"'.format(output_folder=self.output_folder)

    def output(self):
        return {
            'vis_metadata_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'vis-metadata-folder', 'from': 'visualization',
                'to': pathlib.Path(self.execution_folder, 'visualization').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'output_folder': self.output_folder}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.268'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateVsf(QueenbeeTask):
    """Translate a Honeybee Model to a visualization format.

    This can be either a VisualizationSet File (.vsf) in JSON or binary Pkl format
    or it can be a VTKJS file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def active_grid_data(self):
        return 'pass-fail-combined'

    @property
    def output_format(self):
        return 'vsf'

    attr_format = luigi.Parameter(default='text')

    color_by = luigi.Parameter(default='type')

    color_visibility = luigi.Parameter(default='hide')

    face_attr = luigi.Parameter(default='')

    grid_data_display_mode = luigi.Parameter(default='Surface')

    grid_display_mode = luigi.Parameter(default='Default')

    grid_visibility = luigi.Parameter(default='hide')

    room_attr = luigi.Parameter(default='')

    wireframe = luigi.Parameter(default='wireframe')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid_data(self):
        try:
            pathlib.Path('visualization')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('visualization')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_vsf.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-display model-to-vis model.hbjson --color-by {color_by} --{color_visibility}-color-by --{wireframe} --{attr_format}-attr --room-attr "{room_attr}" --face-attr "{face_attr}" --grid-display-mode {grid_display_mode} --{grid_visibility}-grid --grid-data input_data --grid-data-display-mode {grid_data_display_mode} --active-grid-data "{active_grid_data}" --output-format {output_format} --output-file model_vis.{output_format}'.format(face_attr=self.face_attr, grid_display_mode=self.grid_display_mode, active_grid_data=self.active_grid_data, wireframe=self.wireframe, grid_visibility=self.grid_visibility, output_format=self.output_format, attr_format=self.attr_format, grid_data_display_mode=self.grid_data_display_mode, color_visibility=self.color_visibility, color_by=self.color_by, room_attr=self.room_attr)

    def requires(self):
        return {'CopyIlluminance9am': CopyIlluminance9am(_input_params=self._input_params), 'CopyIlluminance3pm': CopyIlluminance3pm(_input_params=self._input_params), 'CopyPassFail9am': CopyPassFail9am(_input_params=self._input_params), 'CopyPassFail3pm': CopyPassFail3pm(_input_params=self._input_params), 'CopyPassFailCombined': CopyPassFailCombined(_input_params=self._input_params), 'CreateVisMetadata': CreateVisMetadata(_input_params=self._input_params)}

    def output(self):
        return {
            'output_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False},
            {'name': 'grid_data', 'to': 'input_data', 'from': self.grid_data, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-file', 'from': 'model_vis.{output_format}'.format(output_format=self.output_format),
                'to': pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'active_grid_data': self.active_grid_data,
            'output_format': self.output_format,
            'attr_format': self.attr_format,
            'color_by': self.color_by,
            'color_visibility': self.color_visibility,
            'face_attr': self.face_attr,
            'grid_data_display_mode': self.grid_data_display_mode,
            'grid_display_mode': self.grid_display_mode,
            'grid_visibility': self.grid_visibility,
            'room_attr': self.room_attr,
            'wireframe': self.wireframe}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-display:0.3.4'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _LeedDaylightOptionTwoVisualization_0c3ede2fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateVsf(_input_params=self.input_values)]
