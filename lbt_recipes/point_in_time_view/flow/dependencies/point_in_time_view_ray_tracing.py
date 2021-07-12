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


_default_inputs = {   'bsdfs': None,
    'metric': 'luminance',
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -aa 0.1 -ad 2048 -ar 64',
    'resolution': 512,
    'simulation_folder': '.',
    'skip_overture': 'overture',
    'view': None,
    'view_count': None,
    'view_name': None}


class MergeResults(QueenbeeTask):
    """Merge several .HDR image files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['view_name']

    @property
    def extension(self):
        return '.unf'

    @property
    def scale_factor(self):
        return '2'

    @property
    def folder(self):
        value = pathlib.Path('results')
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
        return 'honeybee-radiance view merge input_folder view {extension} --scale-factor {scale_factor} --name {name}'.format(extension=self.extension, scale_factor=self.scale_factor, name=self.name)

    def requires(self):
        return {'RayTracing': RayTracing(_input_params=self._input_params)}

    def output(self):
        return {
            'result_image': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../../results/{name}.HDR'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'input_folder', 'from': self.folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-image', 'from': '{name}.HDR'.format(name=self.name),
                'to': pathlib.Path(self.execution_folder, '../../results/{name}.HDR'.format(name=self.name)).resolve().as_posix()
            }]


class RayTracingLoop(QueenbeeTask):
    """Run ray-tracing with rpict command for an input octree and a view file.."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def metric(self):
        return self._input_params['metric']

    @property
    def resolution(self):
        return self._input_params['resolution']

    @property
    def scale_factor(self):
        return '2'

    @property
    def ambient_cache(self):
        try:
            pathlib.Path(self.input()['SplitView']['ambient_cache'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['SplitView']['ambient_cache'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view(self):
        value = pathlib.Path(self.input()['SplitView']['output_folder'].path, self.item['path'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self._input_params['bsdfs'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['bsdfs'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'results').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance rpict rpict scene.oct view.vf --rad-params "{radiance_parameters}" --metric {metric} --resolution {resolution} --scale-factor {scale_factor} --output view.HDR'.format(radiance_parameters=self.radiance_parameters, metric=self.metric, resolution=self.resolution, scale_factor=self.scale_factor)

    def requires(self):
        return {'SplitView': SplitView(_input_params=self._input_params)}

    def output(self):
        return {
            'result_image': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{item_name}.unf'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'ambient_cache', 'to': 'view.amb', 'from': self.ambient_cache, 'optional': True},
            {'name': 'view', 'to': 'view.vf', 'from': self.view, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-image', 'from': 'view.HDR',
                'to': pathlib.Path(self.execution_folder, '{item_name}.unf'.format(item_name=self.item['name'])).resolve().as_posix()
            }]


class RayTracing(luigi.Task):
    """Run ray-tracing with rpict command for an input octree and a view file.."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def views_list(self):
        value = pathlib.Path(self.input()['SplitView']['views_list'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.views_list)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['SplitView']['views_list'].path).as_posix()

    def run(self):
        yield [RayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'ray_tracing.done')
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
        return {'SplitView': SplitView(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'ray_tracing.done').resolve().as_posix())
        }


class SplitView(QueenbeeTask):
    """Split a single view file (.vf) into multiple smaller views."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def view_count(self):
        return self._input_params['view_count']

    @property
    def overture(self):
        return self._input_params['skip_overture']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def input_view(self):
        value = pathlib.Path(self._input_params['view'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        try:
            pathlib.Path(self._input_params['octree_file'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['octree_file'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self._input_params['bsdfs'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['bsdfs'])
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
        return 'honeybee-radiance view split view.vf {view_count} --{overture} --octree {scene_file} --rad-params "{radiance_parameters}" --folder output --log-file output/views_info.json'.format(view_count=self.view_count, overture=self.overture, scene_file=self.scene_file, radiance_parameters=self.radiance_parameters)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'sub_views').resolve().as_posix()
            ),
            
            'ambient_cache': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'sub_views/view.amb').resolve().as_posix()
            ),
            'views_list': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output/views_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_view', 'to': 'view.vf', 'from': self.input_view, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': True},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output',
                'to': pathlib.Path(self.execution_folder, 'sub_views').resolve().as_posix()
            },
                
            {
                'name': 'ambient-cache', 'from': 'output/view.amb',
                'to': pathlib.Path(self.execution_folder, 'sub_views/view.amb').resolve().as_posix()
            }]

    @property
    def output_parameters(self):
        return [{'name': 'views-list', 'from': 'output/views_info.json', 'to': pathlib.Path(self.params_folder, 'output/views_info.json').resolve().as_posix()}]


class _PointInTimeViewRayTracing_ebabebe8Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [MergeResults(_input_params=self.input_values)]
