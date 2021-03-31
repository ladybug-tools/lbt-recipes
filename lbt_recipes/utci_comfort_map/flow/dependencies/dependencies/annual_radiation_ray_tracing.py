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
from queenbee_local import QueenbeeTask


_default_inputs = {   'grid_name': None,
    'octree_file': None,
    'octree_file_with_suns': None,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.',
    'sky_dome': None,
    'sky_matrix_indirect': None,
    'sun_modifiers': None}


class DirectSunlightLoop(QueenbeeTask):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers
    using rcontrib command."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def fixed_radiance_parameters(self):
        return '-aa 0.0 -I -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0'

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def conversion(self):
        return '0.265 0.670 0.065'

    @property
    def output_format(self):
        return 'a'

    calculate_values = luigi.Parameter(default='value')

    order_by = luigi.Parameter(default='sensor')

    @property
    def modifiers(self):
        value = self._input_params['sun_modifiers'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['SplitGrid']['output_folder'].path, self.item['path']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def scene_file(self):
        value = self._input_params['octree_file_with_suns'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], '01_direct').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance dc scontrib scene.oct grid.pts suns.mod --{calculate_values} --sensor-count {sensor_count} --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --output results.ill --order-by-{order_by}'.format(calculate_values=self.calculate_values, sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, conversion=self.conversion, output_format=self.output_format, order_by=self.order_by)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'modifiers', 'to': 'suns.mod', 'from': self.modifiers, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class DirectSunlight(luigi.Task):
    """Calculate daylight contribution for a grid of sensors from a series of modifiers
    using rcontrib command."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = self.input()['SplitGrid']['grids_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return self.input()['SplitGrid']['grids_list'].path

    def run(self):
        yield [DirectSunlightLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'direct_sunlight.done'), 'w') as out_file:
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
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'direct_sunlight.done'))
        }


class IndirectSkyLoop(QueenbeeTask):
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

    order_by = luigi.Parameter(default='sensor')

    output_format = luigi.Parameter(default='f')

    @property
    def sky_matrix(self):
        value = self._input_params['sky_matrix_indirect'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sky_dome(self):
        value = self._input_params['sky_dome'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sensor_grid(self):
        value = os.path.join(self.input()['SplitGrid']['output_folder'].path, self.item['path']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def scene_file(self):
        value = self._input_params['octree_file'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], '02_indirect').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx --sensor-count {sensor_count} --output results.ill --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --conversion "{conversion}" --output-format {output_format} --order-by-{order_by}'.format(sensor_count=self.sensor_count, radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters, conversion=self.conversion, output_format=self.output_format, order_by=self.order_by)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sky_matrix', 'to': 'sky.mtx', 'from': self.sky_matrix, 'optional': False},
            {'name': 'sky_dome', 'to': 'sky.dome', 'from': self.sky_dome, 'optional': False},
            {'name': 'sensor_grid', 'to': 'grid.pts', 'from': self.sensor_grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': 'results.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class IndirectSky(luigi.Task):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = self.input()['SplitGrid']['grids_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return self.input()['SplitGrid']['grids_list'].path

    def run(self):
        yield [IndirectSkyLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'indirect_sky.done'), 'w') as out_file:
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
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'indirect_sky.done'))
        }


class MergeDirectResults(QueenbeeTask):
    """Merge several files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return '.ill'

    @property
    def folder(self):
        value = '01_direct'.replace('\\', '/')
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
        return 'honeybee-radiance grid merge input_folder grid {extension} --name {name}'.format(extension=self.extension, name=self.name)

    def requires(self):
        return {'OutputMatrixMath': OutputMatrixMath(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '../../results/direct/{name}.ill'.format(name=self.name))
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
                'to': os.path.join(self.execution_folder, '../../results/direct/{name}.ill'.format(name=self.name))
            }]


class MergeTotalResults(QueenbeeTask):
    """Merge several files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return '.ill'

    @property
    def folder(self):
        value = '03_total'.replace('\\', '/')
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
        return 'honeybee-radiance grid merge input_folder grid {extension} --name {name}'.format(extension=self.extension, name=self.name)

    def requires(self):
        return {'OutputMatrixMath': OutputMatrixMath(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '../../results/total/{name}.ill'.format(name=self.name))
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
                'to': os.path.join(self.execution_folder, '../../results/total/{name}.ill'.format(name=self.name))
            }]


class OutputMatrixMathLoop(QueenbeeTask):
    """Add indirect sky to direct sunlight."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    conversion = luigi.Parameter(default=' ')

    header = luigi.Parameter(default='remove')

    output_format = luigi.Parameter(default='a')

    @property
    def indirect_sky_matrix(self):
        value = '02_indirect/{item_name}.ill'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sunlight_matrix(self):
        value = '01_direct/{item_name}.ill'.format(item_name=self.item['name']).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], '03_total').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'honeybee-radiance mtxop operate-two sky.ill sun.ill --operator + --{header}-header --conversion "{conversion}" --output-mtx final.ill --output-format {output_format}'.format(header=self.header, conversion=self.conversion, output_format=self.output_format)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params), 'DirectSunlight': DirectSunlight(_input_params=self._input_params), 'IndirectSky': IndirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'results_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'indirect_sky_matrix', 'to': 'sky.ill', 'from': self.indirect_sky_matrix, 'optional': False},
            {'name': 'sunlight_matrix', 'to': 'sun.ill', 'from': self.sunlight_matrix, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-file', 'from': 'final.ill',
                'to': os.path.join(self.execution_folder, '{item_name}.ill'.format(item_name=self.item['name']))
            }]


class OutputMatrixMath(luigi.Task):
    """Add indirect sky to direct sunlight."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = self.input()['SplitGrid']['grids_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return self.input()['SplitGrid']['grids_list'].path

    def run(self):
        yield [OutputMatrixMathLoop(item=item, _input_params=self._input_params) for item in self.items]
        os.makedirs(self.execution_folder, exist_ok=True)
        with open(os.path.join(self.execution_folder, 'output_matrix_math.done'), 'w') as out_file:
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
        return {'SplitGrid': SplitGrid(_input_params=self._input_params), 'DirectSunlight': DirectSunlight(_input_params=self._input_params), 'IndirectSky': IndirectSky(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'output_matrix_math.done'))
        }


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
        value = self._input_params['sensor_grid'].replace('\\', '/')
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
        return 'honeybee-radiance grid split grid.pts {sensor_count} --folder output --log-file output/grids_info.json'.format(sensor_count=self.sensor_count)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, '00_sub_grids')
            ),
            'grids_list': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'output/grids_info.json')
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
                'to': os.path.join(self.execution_folder, '00_sub_grids')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'grids-list', 'from': 'output/grids_info.json', 'to': os.path.join(self.params_folder, 'output/grids_info.json')}]


class _AnnualRadiationRayTracing_7b93ed3aOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [MergeDirectResults(_input_params=self.input_values), MergeTotalResults(_input_params=self.input_values)]
