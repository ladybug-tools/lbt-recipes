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


_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'min_sensor_count': 1,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'simulation_folder': '.',
    'sky_density': 1,
    'timestep': 1,
    'wea': None}


class AccumulateResultsLoop(QueenbeeTask):
    """Postprocess average irradiance (W/m2) into cumulative radiation (kWh/m2)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def timestep(self):
        return self._input_params['timestep']

    @property
    def average_irradiance(self):
        value = pathlib.Path(self.input()['RestructureResults']['output_folder'].path, '{item_name}.res'.format(item_name=self.item['name']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
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

    def command(self):
        return 'honeybee-radiance post-process cumulative-radiation avg_irr.mtx weather.wea --timestep {timestep} --output radiation.mtx'.format(timestep=self.timestep)

    def requires(self):
        return {'RestructureResults': RestructureResults(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'radiation': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/cumulative_radiation/{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/cumulative_radiation/{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class AccumulateResults(luigi.Task):
    """Postprocess average irradiance (W/m2) into cumulative radiation (kWh/m2)."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['CreateRadFolder']['sensor_grids'].path).as_posix()

    def run(self):
        yield [AccumulateResultsLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'accumulate_results.done')
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
        return {'RestructureResults': RestructureResults(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'accumulate_results.done').resolve().as_posix())
        }


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
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
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/cumulative_radiation/grids_info.json').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/cumulative_radiation/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder."""

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
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out}'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False}]

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
    def grid_filter(self):
        return self._input_params['grid_filter']

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
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'bsdf_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/average_irradiance/grids_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/grid/_info.json').resolve().as_posix()
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
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/average_irradiance/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'model/grid/_info.json').resolve().as_posix()}]


class CreateSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'total'

    @property
    def output_type(self):
        return 'solar'

    @property
    def output_format(self):
        return 'ASCII'

    @property
    def sky_density(self):
        return self._input_params['sky_density']

    @property
    def cumulative(self):
        return 'cumulative'

    sun_up_hours = luigi.Parameter(default='all-hours')

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
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(north=self.north, sky_type=self.sky_type, cumulative=self.cumulative, sun_up_hours=self.sun_up_hours, output_type=self.output_type, output_format=self.output_format, sky_density=self.sky_density)

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'resources/sky.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateSkyDome(QueenbeeTask):
    """Create a skydome for daylight coefficient studies."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sky_density(self):
        return self._input_params['sky_density']

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
        return 'honeybee-radiance sky skydome --name rflux_sky.sky --sky-density {sky_density}'.format(sky_density=self.sky_density)

    def output(self):
        return {
            'sky_dome': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-dome', 'from': 'rflux_sky.sky',
                'to': pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class RestructureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def extension(self):
        return 'res'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results')
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
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension}'.format(extension=self.extension)

    def requires(self):
        return {'SkyRadiationRaytracing': SkyRadiationRaytracing(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/average_irradiance').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'results/average_irradiance').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class SkyRadiationRaytracingLoop(QueenbeeTask):
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
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['output_folder'].path, '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
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
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_full_id}'.format(item_full_id=self.item['full_id'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by}'.format(sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, conversion=self.conversion, output_format=self.output_format, order_by=self.order_by)

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'CreateSky': CreateSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': pathlib.Path(self.execution_folder, '../{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class SkyRadiationRaytracing(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['SplitGridFolder']['sensor_grids'].path).as_posix()

    def run(self):
        yield [SkyRadiationRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'sky_radiation_raytracing.done')
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
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'CreateSky': CreateSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'sky_radiation_raytracing.done').resolve().as_posix())
        }


class SplitGridFolder(QueenbeeTask):
    """Create new sensor grids folder with evenly distributed sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def cpus_per_grid(self):
        return '1'

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def input_folder(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid')
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
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder {cpu_count} --grid-divisor {cpus_per_grid} --min-sensor-count {min_sensor_count}'.format(cpu_count=self.cpu_count, cpus_per_grid=self.cpus_per_grid, min_sensor_count=self.min_sensor_count)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/grid').resolve().as_posix()
            ),
            
            'dist_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/_redist_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output_folder/_info.json').resolve().as_posix()
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
                'to': pathlib.Path(self.execution_folder, 'resources/grid').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dist-info', 'from': 'output_folder/_redist_info.json',
                'to': pathlib.Path(self.execution_folder, 'initial_results/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'output_folder/_info.json', 'to': pathlib.Path(self.params_folder, 'output_folder/_info.json').resolve().as_posix()}]


class _Main_e9c43459Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [AccumulateResults(_input_params=self.input_values), CopyGridInfo(_input_params=self.input_values)]
