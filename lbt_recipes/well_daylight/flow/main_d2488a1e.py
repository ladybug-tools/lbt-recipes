"""
This file is auto-generated from well-daylight:0.0.22.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mikkel: mikkel@ladybug.tools
    pollination: info@pollination.solutions

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.well_daylight_visualization import _WellDaylightVisualization_d2488a1eOrchestrator as WellDaylightVisualization_d2488a1eWorkerbee
from .dependencies.main_b46ec90c import _Main_b46ec90cOrchestrator as Main_b46ec90cWorkerbee


_default_inputs = {   'cpu_count': 50,
    'diffuse_transmission': 0.05,
    'epw': None,
    'grid_filter': '*',
    'min_sensor_count': 1000,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05 -dr 0',
    'simulation_folder': '.',
    'specular_transmission': 0.0001}


class AddApertureGroupBlinds(QueenbeeTask):
    """Add a state geometry to aperture groups.

    This command adds state geometry to all aperture groups in the model. The
    geometry is the same as the aperture geometry but the modifier is changed.
    The geometry is translated inward by a distance which by default is 0.001
    in model units."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def diffuse_transmission(self):
        return self._input_params['diffuse_transmission']

    @property
    def specular_transmission(self):
        return self._input_params['specular_transmission']

    distance = luigi.Parameter(default='0.001')

    scale = luigi.Parameter(default='1.005')

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
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'add_aperture_group_blinds.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance multi-phase add-aperture-group-blinds model.hbjson --diffuse-transmission {diffuse_transmission} --specular-transmission {specular_transmission} --distance {distance} --scale {scale} --create-groups --output-model model_blinds.hbjson'.format(diffuse_transmission=self.diffuse_transmission, distance=self.distance, scale=self.scale, specular_transmission=self.specular_transmission)

    def output(self):
        return {
            'output_model': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'output_model.hbjson').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-model', 'from': 'model_blinds.hbjson',
                'to': pathlib.Path(self.execution_folder, 'output_model.hbjson').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'diffuse_transmission': self.diffuse_transmission,
            'specular_transmission': self.specular_transmission,
            'distance': self.distance,
            'scale': self.scale}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.268'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateDaylightHours(QueenbeeTask):
    """Convert EPW to EN 17037 schedule as a CSV file.
    
    This function generates a valid schedule for EN 17037, also known as daylight hours.
    Rather than a typical occupancy schedule, the daylight hours is half the year with
    the largest quantity of daylight."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_daylight_hours.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance schedule epw-to-daylight-hours weather.epw --name daylight_hours'

    def output(self):
        return {
            'daylight_hours_csv': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix()
            ),
            
            'daylight_hours_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'daylight_hours.json').resolve().as_posix()
            ),
            
            'daylight_hours_wea': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'wea.wea').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'daylight-hours-csv', 'from': 'daylight_hours.csv',
                'to': pathlib.Path(self.execution_folder, 'daylight_hours.csv').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'daylight-hours-json', 'from': 'daylight_hours.json',
                'to': pathlib.Path(self.execution_folder, 'daylight_hours.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'daylight-hours-wea', 'from': 'daylight_hours.wea',
                'to': pathlib.Path(self.execution_folder, 'wea.wea').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.66.268'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RunTwoPhaseDaylightCoefficient(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def dtype(self):
        return 'float16'

    timestep = luigi.Parameter(default='1')

    @property
    def model(self):
        value = pathlib.Path(self.input()['AddApertureGroupBlinds']['output_model'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateDaylightHours']['daylight_hours_wea'].path)
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
            'north': self.north,
            'cpu_count': self.cpu_count,
            'min_sensor_count': self.min_sensor_count,
            'radiance_parameters': self.radiance_parameters,
            'grid_filter': self.grid_filter,
            'model': self.model,
            'wea': self.wea,
            'dtype': self.dtype
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [Main_b46ec90cWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').write_text('done!')

    def requires(self):
        return {'CreateDaylightHours': CreateDaylightHours(_input_params=self._input_params), 'AddApertureGroupBlinds': AddApertureGroupBlinds(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_two_phase_daylight_coefficient.done').resolve().as_posix())
        }


class WellAnnualDaylight(QueenbeeTask):
    """Calculate credits for WELL L01 and L06."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    grid_filter = luigi.Parameter(default='*')

    @property
    def folder(self):
        value = pathlib.Path('results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def model(self):
        try:
            pathlib.Path('output_model.hbjson')
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('output_model.hbjson')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def daylight_hours(self):
        value = pathlib.Path(self.input()['CreateDaylightHours']['daylight_hours_csv'].path)
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
        return pathlib.Path(__file__).parent.joinpath('scripts', 'well_annual_daylight.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance-postprocess post-process well well-annual-daylight results daylight_hours.txt --grids-filter " {grid_filter} " --sub-folder well_summary'.format(grid_filter=self.grid_filter)

    def requires(self):
        return {'CreateDaylightHours': CreateDaylightHours(_input_params=self._input_params), 'RunTwoPhaseDaylightCoefficient': RunTwoPhaseDaylightCoefficient(_input_params=self._input_params)}

    def output(self):
        return {
            'well_summary_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'well_summary').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'results', 'from': self.folder, 'optional': False},
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': True},
            {'name': 'daylight_hours', 'to': 'daylight_hours.txt', 'from': self.daylight_hours, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'well-summary-folder', 'from': 'well_summary',
                'to': pathlib.Path(self.execution_folder, 'well_summary').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'grid_filter': self.grid_filter}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance-postprocess:0.4.637'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateVisualization(QueenbeeTask):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path('output_model.hbjson')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def l01_pass_fail(self):
        value = pathlib.Path(self.input()['WellAnnualDaylight']['well_summary_folder'].path, 'ies_lm/pass_fail/L01')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def l06_pass_fail(self):
        value = pathlib.Path(self.input()['WellAnnualDaylight']['well_summary_folder'].path, 'ies_lm/pass_fail/L06')
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
            'l01_pass_fail': self.l01_pass_fail,
            'l06_pass_fail': self.l06_pass_fail
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [WellDaylightVisualization_d2488a1eWorkerbee(_input_params=self.map_dag_inputs)]
        pathlib.Path(self.execution_folder).mkdir(parents=True, exist_ok=True)
        self._copy_output_artifacts(self.execution_folder)
        self._copy_output_parameters(self.execution_folder)
        pathlib.Path(self.execution_folder, 'create_visualization.done').write_text('done!')

    def requires(self):
        return {'RunTwoPhaseDaylightCoefficient': RunTwoPhaseDaylightCoefficient(_input_params=self._input_params), 'WellAnnualDaylight': WellAnnualDaylight(_input_params=self._input_params)}

    def output(self):
        return {
            'visualization': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix()
            ),
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'create_visualization.done').resolve().as_posix())
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'visualization', 'from': 'visualization.vsf',
                'to': pathlib.Path(self.execution_folder, 'visualization.vsf').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _Main_d2488a1eOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CreateVisualization(_input_params=self.input_values)]
