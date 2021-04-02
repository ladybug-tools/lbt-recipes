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
from queenbee_local import QueenbeeTask
from .dependencies.direct_sun_hours_entry_loop import _DirectSunHoursEntryLoop_e811664fOrchestrator as DirectSunHoursEntryLoop_e811664fWorkerbee


_default_inputs = {   'grid_filter': '*',
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'sensor_count': 200,
    'simulation_folder': '.',
    'wea': None}


class ConvertWeaToConstant(QueenbeeTask):
    """Convert a Wea file to have a constant value for each datetime.

    This is useful in workflows where hourly irradiance values are inconsequential
    to the analysis and one is only using the Wea as a format to pass location
    and datetime information (eg. for direct sun hours)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    value = luigi.Parameter(default='1000')

    @property
    def wea(self):
        value = self._input_params['wea'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'ladybug translate wea-to-constant weather.wea --value {value} --output-file constant.wea'.format(value=self.value)

    def output(self):
        return {
            'constant_wea': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/constant.wea')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'constant-wea', 'from': 'constant.wea',
                'to': os.path.join(self.execution_folder, 'resources/constant.wea')
            }]


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to multiple destinations."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = self.input()['CreateRadFolder']['sensor_grids_file'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst_1': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/cumulative/grids_info.json')
            ),
            
            'dst_2': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/direct_radiation/grids_info.json')
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
                'name': 'dst-1', 'from': 'input_path',
                'to': os.path.join(self.execution_folder, 'results/cumulative/grids_info.json')
            },
                
            {
                'name': 'dst-2', 'from': 'input_path',
                'to': os.path.join(self.execution_folder, 'results/direct_radiation/grids_info.json')
            }]


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = self.input()['CreateRadFolder']['model_folder'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sky(self):
        value = self.input()['GenerateSunpath']['sunpath'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/scene_with_suns.oct')
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
                'to': os.path.join(self.execution_folder, 'resources/scene_with_suns.oct')
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
        value = self._input_params['model'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'model')
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/direct_sun_hours/grids_info.json')
            ),
            'sensor_grids': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'model/grid/_info.json')
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
                'to': os.path.join(self.execution_folder, 'model')
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': os.path.join(self.execution_folder, 'results/direct_sun_hours/grids_info.json')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': os.path.join(self.params_folder, 'model/grid/_info.json')}]


class DirectSunHoursRaytracingLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def octree_file(self):
        value = self.input()['CreateOctree']['scene_file'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['CreateRadFolder']['model_folder'].path, 'grid/{item_full_id}.pts'.format(item_full_id=self.item['full_id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sunpath(self):
        value = self.input()['GenerateSunpath']['sunpath'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sun_modifiers(self):
        value = self.input()['GenerateSunpath']['sun_modifiers'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'sensor_count': self.sensor_count,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sunpath': self.sunpath,
            'sun_modifiers': self.sun_modifiers
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DirectSunHoursEntryLoop_e811664fWorkerbee(_input_params=self.map_dag_inputs)]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'direct_sun_hours_raytracing.done'), 'w') as out_file:
            out_file.write('done!\n')

    def requires(self):
        return {'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'direct_sun_hours_raytracing.done'))
        }


class DirectSunHoursRaytracing(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = self.input()['CreateRadFolder']['sensor_grids'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['CreateRadFolder']['sensor_grids'].path

    def run(self):
        yield [DirectSunHoursRaytracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'direct_sun_hours_raytracing.done'), 'w') as out_file:
            out_file.write('done!\n')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def requires(self):
        return {'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'direct_sun_hours_raytracing.done'))
        }


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def output_type(self):
        return '1'

    @property
    def wea(self):
        value = self.input()['ConvertWeaToConstant']['constant_wea'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(output_type=self.output_type, north=self.north)

    def requires(self):
        return {'ConvertWeaToConstant': ConvertWeaToConstant(_input_params=self._input_params)}

    def output(self):
        return {
            'sunpath': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/sunpath.mtx')
            ),
            
            'sun_modifiers': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'resources/suns.mod')
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
                'name': 'sunpath', 'from': 'sunpath.mtx',
                'to': os.path.join(self.execution_folder, 'resources/sunpath.mtx')
            },
                
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': os.path.join(self.execution_folder, 'resources/suns.mod')
            }]


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    leap_year = luigi.Parameter(default='full-year')

    timestep = luigi.Parameter(default='1')

    @property
    def sun_modifiers(self):
        value = self.input()['GenerateSunpath']['sun_modifiers'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt --timestep {timestep} --{leap_year}'.format(timestep=self.timestep, leap_year=self.leap_year)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/direct_sun_hours/sun-up-hours.txt')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': os.path.join(self.execution_folder, 'results/direct_sun_hours/sun-up-hours.txt')
            }]


class _Main_e811664fOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [CopyGridInfo(_input_params=self.input_values), DirectSunHoursRaytracing(_input_params=self.input_values), ParseSunUpHours(_input_params=self.input_values)]
