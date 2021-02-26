import luigi
import os
from queenbee_local import QueenbeeTask
from .dependencies.main import _Main_12f6f064Orchestrator as Main_12f6f064Workerbee


_default_inputs = {   'comfort_parameters': '--ppd-threshold 10',
    'ddy': None,
    'epw': None,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'run_period': '',
    'sensor_count': 200,
    'simulation_folder': '.',
    'solarcal_parameters': '--posture seated --sharp 135 --absorptivity 0.7 '
                           '--emissivity 0.95',
    'write_set_map': 'write-op-map'}


class CreateResultInfo(QueenbeeTask):
    """Get a JSON that specifies the data type and units for comfort map outputs."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def comfort_model(self):
        return 'pmv'

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def qualifier(self):
        return self._input_params['write_set_map']

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
        return 'ladybug-comfort map map-result-info {comfort_model} --run-period "{run_period}" --qualifier "{qualifier}" --output-file results_info.json'.format(comfort_model=self.comfort_model, run_period=self.run_period, qualifier=self.qualifier)

    def output(self):
        return {
            'results_info_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/results_info.json')
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results-info-file', 'from': 'results_info.json',
                'to': os.path.join(self.execution_folder, 'results/results_info.json')
            }]


class CreateSimPar(QueenbeeTask):
    """Get a SimulationParameter JSON with all outputs for thermal comfort mapping."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def north(self):
        return self._input_params['north']

    filter_des_days = luigi.Parameter(default='filter-des-days')

    @property
    def ddy(self):
        value = self._input_params['ddy'].replace('\\', '/')
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
        return 'honeybee-energy settings comfort-sim-par input.ddy --run-period "{run_period}" --north {north} --{filter_des_days} --output-file sim_par.json'.format(run_period=self.run_period, north=self.north, filter_des_days=self.filter_des_days)

    def output(self):
        return {
            'sim_par_json': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'energy/simulation_parameter.json')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'ddy', 'to': 'input.ddy', 'from': self.ddy}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sim-par-json', 'from': 'sim_par.json',
                'to': os.path.join(self.execution_folder, 'energy/simulation_parameter.json')
            }]


class CreateWea(QueenbeeTask):
    """Translate an .epw file to a .wea file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    timestep = luigi.Parameter(default='1')

    @property
    def epw(self):
        value = self._input_params['epw'].replace('\\', '/')
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
        return 'ladybug translate epw-to-wea weather.epw --analysis-period "{period}" --timestep {timestep} --output-file weather.wea'.format(period=self.period, timestep=self.timestep)

    def output(self):
        return {
            'wea': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'in.wea')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'wea', 'from': 'weather.wea',
                'to': os.path.join(self.execution_folder, 'in.wea')
            }]


class GetEnclosureInfo(QueenbeeTask):
    """Create JSONs with radiant enclosure information from a HBJSON input file.

    This enclosure info is intended to be consumed by thermal mapping functions."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def model(self):
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
        return 'honeybee-radiance translate model-radiant-enclosure-info model.hbjson --folder output --log-file enclosure_list.json'

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'radiance/enclosures')
            ),
            
            'enclosure_list_file': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'results/grids_info.json')
            ),
            'enclosure_list': luigi.LocalTarget(
                os.path.join(
                    self.params_folder,
                    'enclosure_list.json')
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output',
                'to': os.path.join(self.execution_folder, 'radiance/enclosures')
            },
                
            {
                'name': 'enclosure-list-file', 'from': 'enclosure_list.json',
                'to': os.path.join(self.execution_folder, 'results/grids_info.json')
            }]

    @property
    def output_parameters(self):
        return [{'name': 'enclosure-list', 'from': 'enclosure_list.json', 'to': os.path.join(self.params_folder, 'enclosure_list.json')}]


class MirrorSensorGrids(QueenbeeTask):
    """Mirror a honeybee Model's SensorGrids and format them for thermal mapping.

    This involves setting the direction of every sensor to point up (0, 0, 1) and
    then adding a mirrored sensor grid with the same sensor positions that all
    point downward. In thermal mapping workflows, the upward-pointing grids are
    used to account for direct and diffuse shortwave irradiance while the
    downard pointing grids account for ground-reflected shortwave irradiance."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def model(self):
        value = self.input()['SetModifiersFromConstructions']['new_model'].path.replace('\\', '/')
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
        return 'honeybee-radiance edit mirror-model-sensors model.hbjson --output-file new_model.hbjson'

    def requires(self):
        return {'SetModifiersFromConstructions': SetModifiersFromConstructions(_input_params=self._input_params)}

    def output(self):
        return {
            'new_model': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'radiance/hbjson/2_mirrored_grids.hbjson')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'new-model', 'from': 'new_model.hbjson',
                'to': os.path.join(self.execution_folder, 'radiance/hbjson/2_mirrored_grids.hbjson')
            }]


class RunComfortMapLoop(QueenbeeTask):
    """Get CSV files with maps of PMV comfort from EnergyPlus and Radiance results."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def air_speed(self):
        return self._input_params['air_speed']

    @property
    def met_rate(self):
        return self._input_params['met_rate']

    @property
    def clo_value(self):
        return self._input_params['clo_value']

    @property
    def solarcal_par(self):
        return self._input_params['solarcal_parameters']

    @property
    def comfort_par(self):
        return self._input_params['comfort_parameters']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def write_set_map(self):
        return self._input_params['write_set_map']

    @property
    def result_sql(self):
        value = self.input()['RunEnergySimulation']['sql'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def enclosure_info(self):
        value = os.path.join(self.input()['GetEnclosureInfo']['output_folder'].path, '{item_id}.json'.format(item_id=self.item['id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def epw(self):
        value = self._input_params['epw'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def total_irradiance(self):
        value = os.path.join('radiance/shortwave/results/total', '{item_id}.ill'.format(item_id=self.item['id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def direct_irradiance(self):
        value = os.path.join('radiance/shortwave/results/direct', '{item_id}.ill'.format(item_id=self.item['id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def ref_irradiance(self):
        value = os.path.join('radiance/shortwave/results/total', '{item_id}_ref.ill'.format(item_id=self.item['id'])).replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sun_up_hours(self):
        value = os.path.join('radiance/shortwave/results/total', 'sun-up-hours.txt').replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'results').replace('\\', '/')

    @property
    def initiation_folder(self):
        return self._input_params['simulation_folder'].replace('\\', '/')

    @property
    def params_folder(self):
        return os.path.join(self.execution_folder, self._input_params['params_folder']).replace('\\', '/')

    def command(self):
        return 'ladybug-comfort map pmv result.sql enclosure_info.json weather.epw --total-irradiance total.ill --direct-irradiance direct.ill --ref-irradiance ref.ill --sun-up-hours sun-up-hours.txt --air-speed "{air_speed}" --met-rate "{met_rate}" --clo-value "{clo_value}" --solarcal-par "{solarcal_par}" --comfort-par "{comfort_par}" --run-period "{run_period}" --{write_set_map}  --folder output'.format(air_speed=self.air_speed, met_rate=self.met_rate, clo_value=self.clo_value, solarcal_par=self.solarcal_par, comfort_par=self.comfort_par, run_period=self.run_period, write_set_map=self.write_set_map)

    def requires(self):
        return {'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunIrradianceSimulation': RunIrradianceSimulation(_input_params=self._input_params), 'GetEnclosureInfo': GetEnclosureInfo(_input_params=self._input_params)}

    def output(self):
        return {
            'temperature_map': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'temperature/{item_id}.csv'.format(item_id=self.item['id']))
            ),
            
            'condition_map': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'condition/{item_id}.csv'.format(item_id=self.item['id']))
            ),
            
            'pmv_map': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'condition_intensity/{item_id}.csv'.format(item_id=self.item['id']))
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'result_sql', 'to': 'result.sql', 'from': self.result_sql},
            {'name': 'enclosure_info', 'to': 'enclosure_info.json', 'from': self.enclosure_info},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw},
            {'name': 'total_irradiance', 'to': 'total.ill', 'from': self.total_irradiance},
            {'name': 'direct_irradiance', 'to': 'direct.ill', 'from': self.direct_irradiance},
            {'name': 'ref_irradiance', 'to': 'ref.ill', 'from': self.ref_irradiance},
            {'name': 'sun_up_hours', 'to': 'sun-up-hours.txt', 'from': self.sun_up_hours}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'temperature-map', 'from': 'output/temperature.csv',
                'to': os.path.join(self.execution_folder, 'temperature/{item_id}.csv'.format(item_id=self.item['id']))
            },
                
            {
                'name': 'condition-map', 'from': 'output/condition.csv',
                'to': os.path.join(self.execution_folder, 'condition/{item_id}.csv'.format(item_id=self.item['id']))
            },
                
            {
                'name': 'pmv-map', 'from': 'output/condition_intensity.csv',
                'to': os.path.join(self.execution_folder, 'condition_intensity/{item_id}.csv'.format(item_id=self.item['id']))
            }]


class RunComfortMap(luigi.Task):
    """Get CSV files with maps of PMV comfort from EnergyPlus and Radiance results."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def enclosure_list(self):
        value = self.input()['GetEnclosureInfo']['enclosure_list'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.enclosure_list)
        except:
            # it is a parameter
            return self.input()['GetEnclosureInfo']['enclosure_list'].path

    def run(self):
        yield [RunComfortMapLoop(item=item, _input_params=self._input_params) for item in self.items]
        with open(os.path.join(self.execution_folder, 'run_comfort_map.done'), 'w') as out_file:
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
        return {'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunIrradianceSimulation': RunIrradianceSimulation(_input_params=self._input_params), 'GetEnclosureInfo': GetEnclosureInfo(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'run_comfort_map.done'))
        }


class RunEnergySimulation(QueenbeeTask):
    """Simulate a Model JSON file in EnergyPlus."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def model(self):
        value = self._input_params['model'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def epw(self):
        value = self._input_params['epw'].replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def sim_par(self):
        value = self.input()['CreateSimPar']['sim_par_json'].path.replace('\\', '/')
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
        return 'honeybee-energy simulate model model.hbjson weather.epw --sim-par-json sim-par.json --folder output'

    def requires(self):
        return {'CreateSimPar': CreateSimPar(_input_params=self._input_params)}

    def output(self):
        return {
            'sql': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'energy/eplusout.sql')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw},
            {'name': 'sim_par', 'to': 'sim-par.json', 'from': self.sim_par}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sql', 'from': 'output/run/eplusout.sql',
                'to': os.path.join(self.execution_folder, 'energy/eplusout.sql')
            }]


class RunIrradianceSimulation(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    sensor_grid = luigi.Parameter(default='*')

    @property
    def model(self):
        value = self.input()['MirrorSensorGrids']['new_model'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def wea(self):
        value = self.input()['CreateWea']['wea'].path.replace('\\', '/')
        return value if os.path.isabs(value) \
            else os.path.join(self.initiation_folder, value)

    @property
    def execution_folder(self):
        return os.path.join(self._input_params['simulation_folder'], 'radiance/shortwave').replace('\\', '/')

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
            'model': self.model,
            'wea': self.wea,
            'north': self.north,
            'sensor_count': self.sensor_count,
            'radiance_parameters': self.radiance_parameters
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [Main_12f6f064Workerbee(_input_params=self.map_dag_inputs)]
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        with open(os.path.join(self.execution_folder, 'run_irradiance_simulation.done'), 'w') as out_file:
            out_file.write('done!\n')

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params), 'MirrorSensorGrids': MirrorSensorGrids(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(os.path.join(self.execution_folder, 'run_irradiance_simulation.done'))
        }


class SetModifiersFromConstructions(QueenbeeTask):
    """Assign honeybee Radiance modifiers based on energy construction properties."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def use_visible(self):
        return 'solar'

    @property
    def exterior_offset(self):
        return '0.03'

    @property
    def model(self):
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
        return 'honeybee-energy edit modifiers-from-constructions model.hbjson --{use_visible} --exterior-offset {exterior_offset} --output-file new_model.hbjson'.format(use_visible=self.use_visible, exterior_offset=self.exterior_offset)

    def output(self):
        return {
            'new_model': luigi.LocalTarget(
                os.path.join(self.execution_folder, 'radiance/hbjson/1_energy_modifiers.hbjson')
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'new-model', 'from': 'new_model.hbjson',
                'to': os.path.join(self.execution_folder, 'radiance/hbjson/1_energy_modifiers.hbjson')
            }]


class _Main_de7c0435Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        return [CreateResultInfo(_input_params=self.input_values), RunComfortMap(_input_params=self.input_values)]