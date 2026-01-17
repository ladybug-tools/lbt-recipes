"""
This file is auto-generated from point-in-time-view:0.5.0.
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
from .dependencies.point_in_time_view_ray_tracing import _PointInTimeViewRayTracing_8480f42eOrchestrator as PointInTimeViewRayTracing_8480f42eWorkerbee
from .dependencies.point_in_time_view_prepare_folder import _PointInTimeViewPrepareFolder_8480f42eOrchestrator as PointInTimeViewPrepareFolder_8480f42eWorkerbee


_default_inputs = {   'cpu_count': 12,
    'metric': 'luminance',
    'model': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -aa 0.25 -ad 512 -ar 16',
    'resolution': 800,
    'simulation_folder': '.',
    'skip_overture': 'overture',
    'sky': None,
    'view_filter': '*'}


class PrepareFolderPointInTimeView(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def sky(self):
        return self._input_params['sky']

    @property
    def metric(self):
        return self._input_params['metric']

    @property
    def resolution(self):
        return self._input_params['resolution']

    @property
    def view_filter(self):
        return self._input_params['view_filter']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    radiance_parameters = luigi.Parameter(default='-ab 2 -aa 0.25 -ad 512 -ar 16')

    skip_overture = luigi.Parameter(default='overture')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
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
            'sky': self.sky,
            'metric': self.metric,
            'resolution': self.resolution,
            'view_filter': self.view_filter,
            'cpu_count': self.cpu_count
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [PointInTimeViewPrepareFolder_8480f42eWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'prepare_folder_point_in_time_view.done').write_text('done!')

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
            'views': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'results/views_info.json').resolve().as_posix()
                ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'prepare_folder_point_in_time_view.done').resolve().as_posix())
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
        return [{'name': 'views', 'from': 'results/views_info.json', 'to': pathlib.Path(self.params_folder, 'results/views_info.json').resolve().as_posix()}]


class ComputeViewSplitCount(QueenbeeTask):
    """Get the number of times to split each view in a model using a CPU count."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def views_file(self):
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['results'].path, 'views_info.json')
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'compute_view_split_count.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance view split-count view_info.json {cpu_count} --output-file view-split-count.txt'.format(cpu_count=self.cpu_count)

    def requires(self):
        return {'PrepareFolderPointInTimeView': PrepareFolderPointInTimeView(_input_params=self._input_params)}

    def output(self):
        return {'split_count': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'view-split-count.txt').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'views_file', 'to': 'view_info.json', 'from': self.views_file, 'optional': False}]

    @property
    def input_parameters(self):
        return {
            'cpu_count': self.cpu_count}

    @property
    def output_parameters(self):
        return [{'name': 'split-count', 'from': 'view-split-count.txt', 'to': pathlib.Path(self.params_folder, 'view-split-count.txt').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class PointInTimeViewRayTracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def metric(self):
        return self._input_params['metric']

    @property
    def resolution(self):
        return self._input_params['resolution']

    @property
    def skip_overture(self):
        return self._input_params['skip_overture']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def view_count(self):
        return qb_load_input_param(
                self.input()['ComputeViewSplitCount']['split_count'].path
            )

    @property
    def view_name(self):
        return self.item['full_id']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['resources'].path, 'scene.oct')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view(self):
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['model_folder'].path, 'view/{item_full_id}.vf'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['PrepareFolderPointInTimeView']['model_folder'].path, 'bsdf')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['model_folder'].path, 'bsdf')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ies(self):
        try:
            pathlib.Path(self.input()['PrepareFolderPointInTimeView']['model_folder'].path, 'ies')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['model_folder'].path, 'ies')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).resolve().as_posix()

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
            'metric': self.metric,
            'resolution': self.resolution,
            'skip_overture': self.skip_overture,
            'radiance_parameters': self.radiance_parameters,
            'view_count': self.view_count,
            'octree_file': self.octree_file,
            'view_name': self.view_name,
            'view': self.view,
            'bsdfs': self.bsdfs,
            'ies': self.ies
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [PointInTimeViewRayTracing_8480f42eWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'PrepareFolderPointInTimeView': PrepareFolderPointInTimeView(_input_params=self._input_params), 'ComputeViewSplitCount': ComputeViewSplitCount(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done').resolve().as_posix())
        }


class PointInTimeViewRayTracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def views(self):
        value = pathlib.Path(self.input()['PrepareFolderPointInTimeView']['views'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.views)
        except:
            # it is a parameter
            return self.input()['PrepareFolderPointInTimeView']['views'].path

    def run(self):
        yield [PointInTimeViewRayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done')
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
        return {'PrepareFolderPointInTimeView': PrepareFolderPointInTimeView(_input_params=self._input_params), 'ComputeViewSplitCount': ComputeViewSplitCount(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done').resolve().as_posix())
        }


class _Main_8480f42eOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [PointInTimeViewRayTracing(_input_params=self.input_values)]
