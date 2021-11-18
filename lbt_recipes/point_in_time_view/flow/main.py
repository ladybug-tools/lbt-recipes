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
from .dependencies.point_in_time_view_ray_tracing import _PointInTimeViewRayTracing_f677f6a5Orchestrator as PointInTimeViewRayTracing_f677f6a5Workerbee


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


class AdjustSky(QueenbeeTask):
    """Adjust a sky file to ensure it is suitable for a given metric.

    Specifcally, this ensures that skies being created with gendaylit have a -O
    option that aligns with visible vs. solar energy."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def metric(self):
        return self._input_params['metric']

    @property
    def sky(self):
        value = pathlib.Path(self.input()['GenerateSky']['sky'].path)
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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky adjust-for-metric input.sky --metric {metric}'.format(metric=self.metric)

    def requires(self):
        return {'GenerateSky': GenerateSky(_input_params=self._input_params)}

    def output(self):
        return {
            'adjusted_sky': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/weather.sky').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky', 'to': 'input.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'adjusted-sky', 'from': '{metric}.sky'.format(metric=self.metric),
                'to': pathlib.Path(self.execution_folder, 'resources/weather.sky').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class ComputeViewSplitCount(QueenbeeTask):
    """Get the number of times to split each view in a model using a CPU count."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def views_file(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['views_file'].path)
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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance view split-count view_info.json {cpu_count} --output-file view-split-count.txt'.format(cpu_count=self.cpu_count)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

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
    def output_parameters(self):
        return [{'name': 'split-count', 'from': 'view-split-count.txt', 'to': pathlib.Path(self.params_folder, 'view-split-count.txt').resolve().as_posix()}]


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['AdjustSky']['adjusted_sky'].path)
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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'AdjustSky': AdjustSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def view_filter(self):
        return self._input_params['view_filter']

    @property
    def input_model(self):
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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --view "{view_filter}" --view-check'.format(view_filter=self.view_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'bsdf_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            ),
            
            'views_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/views_info.json').resolve().as_posix()
            ),
            'views': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/view/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

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
                'name': 'bsdf-folder', 'from': 'model/bsdf',
                'to': pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix(),
                'optional': True,
                'type': 'folder'
            },
                
            {
                'name': 'views-file', 'from': 'model/view/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/views_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'views', 'from': 'model/view/_info.json', 'to': pathlib.Path(self.params_folder, 'model/view/_info.json').resolve().as_posix()}]


class GenerateSky(QueenbeeTask):
    """Generates a sky from a honeybee-radiance sky string."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sky_string(self):
        return self._input_params['sky']

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky {sky_string} --name output.sky'.format(sky_string=self.sky_string)

    def output(self):
        return {
            'sky': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/weather.sky').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky', 'from': 'output.sky',
                'to': pathlib.Path(self.execution_folder, 'resources/weather.sky').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class PointInTimeViewRayTracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

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
        return QueenbeeTask.load_input_param(
            pathlib.Path(
                self.params_folder, 
                os.path.split(self.input()['ComputeViewSplitCount']['split_count'].path)[-1]
            ).resolve().as_posix()
        )

    @property
    def view_name(self):
        return self.item['full_id']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'view/{item_full_id}.vf'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

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
            'bsdfs': self.bsdfs
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [PointInTimeViewRayTracing_f677f6a5Workerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'ComputeViewSplitCount': ComputeViewSplitCount(_input_params=self._input_params)}

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
        value = pathlib.Path(self.input()['CreateRadFolder']['views'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.views)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['CreateRadFolder']['views'].path).as_posix()

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
        return pathlib.Path(self.initiation_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'ComputeViewSplitCount': ComputeViewSplitCount(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'point_in_time_view_ray_tracing.done').resolve().as_posix())
        }


class _Main_f677f6a5Orchestrator(luigi.WrapperTask):
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
