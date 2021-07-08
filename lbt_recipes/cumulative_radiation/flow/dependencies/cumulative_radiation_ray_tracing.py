"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask


_default_inputs = {   'bsdfs': None,
    'grid_name': None,
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix': None,
    'timestep': 1,
    'wea': None}


class AccumulateResults(QueenbeeTask):
    """Postprocess average irradiance (W/m2) into cumulative radiation (kWh/m2)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def average_irradiance(self):
        value = pathlib.Path(self.input()['MergeResults']['result_file'].path)
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

    def command(self):
        return 'honeybee-radiance post-process cumulative-radiation avg_irr.mtx weather.wea --timestep {timestep} --output radiation.mtx'.format(timestep=self.timestep)

    def requires(self):
        return {'MergeResults': MergeResults(_input_params=self._input_params)}

    def output(self):
        return {
            'radiation': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../../results/cumulative_radiation/{name}.res'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'average_irradiance', 'to': 'avg_irr.mtx', 'from': self.average_irradiance, 'optional': False},
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'radiation', 'from': 'radiation.mtx',
                'to': pathlib.Path(self.execution_folder, '../../results/cumulative_radiation/{name}.res'.format(name=self.name)).resolve().as_posix()
            }]


class MergeResults(QueenbeeTask):
    """Merge several files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return '.res'

    @property
    def folder(self):
        value = pathlib.Path('01_radiation')
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
        return 'honeybee-radiance grid merge input_folder grid  {extension} --name {name}'.format(extension=self.extension, name=self.name)

    def requires(self):
        return {'TotalSky': TotalSky(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../../results/average_irradiance/{name}.res'.format(name=self.name)).resolve().as_posix()
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
                'name': 'result-file', 'from': '{name}{extension}'.format(name=self.name, extension=self.extension),
                'to': pathlib.Path(self.execution_folder, '../../results/average_irradiance/{name}.res'.format(name=self.name)).resolve().as_posix()
            }]


class SplitGrid(QueenbeeTask):
    """Split a single sensor grid file into multiple smaller grids."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def input_grid(self):
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

    def command(self):
        return 'honeybee-radiance grid split grid.pts {sensor_count} --folder output --log-file output/grids_info.json'.format(sensor_count=self.sensor_count)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '00_sub_grids').resolve().as_posix()
            ),
            'grids_list': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output/grids_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_grid', 'to': 'grid.pts', 'from': self.input_grid, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output',
                'to': pathlib.Path(self.execution_folder, '00_sub_grids').resolve().as_posix()
            }]

    @property
    def output_parameters(self):
        return [{'name': 'grids-list', 'from': 'output/grids_info.json', 'to': pathlib.Path(self.params_folder, 'output/grids_info.json').resolve().as_posix()}]


class TotalSkyLoop(QueenbeeTask):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -c 1'

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def output_format(self):
        return 'a'

    order_by = luigi.Parameter(default='sensor')

    @property
    def sky_matrix(self):
        value = pathlib.Path(self._input_params['sky_matrix'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self._input_params['sky_dome'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['SplitGrid']['output_folder'].path, self.item['path'])
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
        return pathlib.Path(self._input_params['simulation_folder'], '01_radiation').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by}'.format(sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, conversion=self.conversion, output_format=self.output_format, order_by=self.order_by)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            }]


class TotalSky(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = pathlib.Path(self.input()['SplitGrid']['grids_list'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['SplitGrid']['grids_list'].path).as_posix()

    def run(self):
        yield [TotalSkyLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'total_sky.done')
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
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'total_sky.done').resolve().as_posix())
        }


class _CumulativeRadiationRayTracing_52de34a8Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [AccumulateResults(_input_params=self.input_values)]
