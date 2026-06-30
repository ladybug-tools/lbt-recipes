"""
This file is auto-generated from annual-daylight-en17037:0.1.24.
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


_default_inputs = {   'grid_metrics': None,
    'model': None,
    'params_folder': '__params',
    'results': None,
    'schedule': None,
    'simulation_folder': '.',
    'thresholds': '-t 300 -lt 100 -ut 3000'}


class CalculateAnnualMetrics(QueenbeeTask):
    """Calculate annual daylight metrics for annual daylight simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def thresholds(self):
        return self._input_params['thresholds']

    @property
    def folder(self):
        value = pathlib.Path(self._input_params['results'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def schedule(self):
        try:
            pathlib.Path(self._input_params['schedule'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['schedule'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'calculate_annual_metrics.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess post-process annual-daylight raw_results --schedule schedule.txt {thresholds} --sub-folder metrics'.format(thresholds=self.thresholds)

    def output(self):
        return {
            'annual_metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False},
            {'name': 'schedule', 'to': 'schedule.txt', 'from': self.schedule, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'annual-metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'thresholds': self.thresholds}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.654'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CalculateAnnualMetricsEn17037(QueenbeeTask):
    """Calculate annual daylight EN 173037 metrics for annual daylight simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def folder(self):
        value = pathlib.Path(self._input_params['results'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def schedule(self):
        value = pathlib.Path(self._input_params['schedule'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'calculate_annual_metrics_en17037.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess post-process annual-daylight-en17037 raw_results schedule.txt --sub_folder metrics'

    def output(self):
        return {
            'annual_en17037_metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'en17037').resolve().as_posix()
            ),
            
            'summary': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'en17037/summary.json').resolve().as_posix()
            ),
            
            'summary_grid': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'en17037/summary_grid.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False},
            {'name': 'schedule', 'to': 'schedule.txt', 'from': self.schedule, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'annual-en17037-metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'en17037').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'summary', 'from': 'metrics/summary.json',
                'to': pathlib.Path(self.execution_folder, 'en17037/summary.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'summary-grid', 'from': 'metrics/summary_grid.json',
                'to': pathlib.Path(self.execution_folder, 'en17037/summary_grid.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.654'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateVsfEn17037(QueenbeeTask):
    """Translate a Honeybee Model to a visualization format.

    This can be either a VisualizationSet File (.vsf) in JSON or binary Pkl format
    or it can be a VTKJS file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def active_grid_data(self):
        return 'target_illuminance_300'

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
            pathlib.Path(self.input()['CalculateAnnualMetricsEn17037']['annual_en17037_metrics'].path, 'da')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CalculateAnnualMetricsEn17037']['annual_en17037_metrics'].path, 'da')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_vsf_en17037.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-display model-to-vis model.hbjson --color-by {color_by} --{color_visibility}-color-by --{wireframe} --{attr_format}-attr --room-attr "{room_attr}" --face-attr "{face_attr}" --grid-display-mode {grid_display_mode} --{grid_visibility}-grid --grid-data input_data --grid-data-display-mode {grid_data_display_mode} --active-grid-data "{active_grid_data}" --output-format {output_format} --output-file model_vis.{output_format}'.format(output_format=self.output_format, color_visibility=self.color_visibility, color_by=self.color_by, face_attr=self.face_attr, grid_display_mode=self.grid_display_mode, room_attr=self.room_attr, grid_visibility=self.grid_visibility, grid_data_display_mode=self.grid_data_display_mode, wireframe=self.wireframe, attr_format=self.attr_format, active_grid_data=self.active_grid_data)

    def requires(self):
        return {'CalculateAnnualMetricsEn17037': CalculateAnnualMetricsEn17037(_input_params=self._input_params)}

    def output(self):
        return {
            'output_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization_en17037.vsf').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'visualization_en17037.vsf').resolve().as_posix(),
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
        return 'docker.io/ladybugtools/honeybee-display:0.5.3'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateVsfMetrics(QueenbeeTask):
    """Translate a Honeybee Model to a visualization format.

    This can be either a VisualizationSet File (.vsf) in JSON or binary Pkl format
    or it can be a VTKJS file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def active_grid_data(self):
        return 'udi'

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
            pathlib.Path(self.input()['CalculateAnnualMetrics']['annual_metrics'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CalculateAnnualMetrics']['annual_metrics'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_vsf_metrics.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-display model-to-vis model.hbjson --color-by {color_by} --{color_visibility}-color-by --{wireframe} --{attr_format}-attr --room-attr "{room_attr}" --face-attr "{face_attr}" --grid-display-mode {grid_display_mode} --{grid_visibility}-grid --grid-data input_data --grid-data-display-mode {grid_data_display_mode} --active-grid-data "{active_grid_data}" --output-format {output_format} --output-file model_vis.{output_format}'.format(output_format=self.output_format, color_visibility=self.color_visibility, color_by=self.color_by, face_attr=self.face_attr, grid_display_mode=self.grid_display_mode, room_attr=self.room_attr, grid_visibility=self.grid_visibility, grid_data_display_mode=self.grid_data_display_mode, wireframe=self.wireframe, attr_format=self.attr_format, active_grid_data=self.active_grid_data)

    def requires(self):
        return {'CalculateAnnualMetrics': CalculateAnnualMetrics(_input_params=self._input_params)}

    def output(self):
        return {
            'output_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization_metrics.vsf').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'visualization_metrics.vsf').resolve().as_posix(),
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
        return 'docker.io/ladybugtools/honeybee-display:0.5.3'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class GridSummaryMetrics(QueenbeeTask):
    """Calculate grid summary for metrics."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def folder_level(self):
        return 'sub-folder'

    @property
    def folder(self):
        value = pathlib.Path(self.input()['CalculateAnnualMetrics']['annual_metrics'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def model(self):
        try:
            pathlib.Path(self._input_params['model'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def grid_metrics(self):
        try:
            pathlib.Path(self._input_params['grid_metrics'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['grid_metrics'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'grid_summary_metrics.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess post-process grid-summary metrics --model model.hbjson --grids-info grids_info.json --grid-metrics grid_metrics.json --{folder_level}'.format(folder_level=self.folder_level)

    def requires(self):
        return {'CalculateAnnualMetrics': CalculateAnnualMetrics(_input_params=self._input_params)}

    def output(self):
        return {
            'grid_summary': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'grid_summary.csv').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'metrics', 'from': self.folder, 'optional': False},
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': True},
            {'name': 'grid_metrics', 'to': 'grid_metrics.json', 'from': self.grid_metrics, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'grid-summary', 'from': 'metrics/grid_summary.csv',
                'to': pathlib.Path(self.execution_folder, 'grid_summary.csv').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'folder_level': self.folder_level}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.654'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _AnnualDaylightEN17037PostProcess_f7730ca9Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateVsfEn17037(_input_params=self.input_values), CreateVsfMetrics(_input_params=self.input_values), GridSummaryMetrics(_input_params=self.input_values)]
