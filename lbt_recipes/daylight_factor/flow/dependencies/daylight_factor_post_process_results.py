"""
This file is auto-generated from daylight-factor:0.8.12.
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
    'grids_info': None,
    'model': None,
    'params_folder': '__params',
    'results_folder': None,
    'simulation_folder': '.'}


class RestructureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'res'

    @property
    def input_folder(self):
        value = pathlib.Path(self._input_params['results_folder'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.64.184'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyGridInfo(QueenbeeTask):
    """Copy a file to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['grids_info'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_grid_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input file...'

    def requires(self):
        return {'RestructureResults': RestructureResults(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
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


class GridSummaryMetrics(QueenbeeTask):
    """Calculate grid summary for metrics."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def folder_level(self):
        return 'main-folder'

    @property
    def folder(self):
        value = pathlib.Path(self.input()['RestructureResults']['output_folder'].path)
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
    def grids_info(self):
        try:
            pathlib.Path(self._input_params['grids_info'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['grids_info'])
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
        return {'RestructureResults': RestructureResults(_input_params=self._input_params)}

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
            {'name': 'grids_info', 'to': 'grids_info.json', 'from': self.grids_info, 'optional': True},
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
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.231'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _DaylightFactorPostProcessResults_0d7cfa1eOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CopyGridInfo(_input_params=self.input_values), GridSummaryMetrics(_input_params=self.input_values)]
