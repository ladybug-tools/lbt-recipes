import sys
import luigi
import os
import time
from multiprocessing import freeze_support
from queenbee_local import local_scheduler, _copy_artifacts, update_params, parse_input_args

import flow.main as pmv_comfort_map_workerbee


_recipe_default_inputs = {   'air_speed': '0.1',
    'clo_value': '0.7',
    'comfort_parameters': '--ppd-threshold 10',
    'ddy': None,
    'epw': None,
    'met_rate': '1.1',
    'model': None,
    'north': 0.0,
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'run_period': '',
    'sensor_count': 200,
    'solarcal_parameters': '--posture seated --sharp 135 --absorptivity 0.7 '
                           '--emissivity 0.95',
    'write_set_map': 'write-op-map'}


class LetPmvComfortMapFly(luigi.WrapperTask):
    # global parameters
    _input_params = luigi.DictParameter()

    def requires(self):
        yield [pmv_comfort_map_workerbee._Main_de7c0435Orchestrator(_input_params=self._input_params)]


def start(project_folder, user_values, workers):
    freeze_support()

    input_params = update_params(_recipe_default_inputs, user_values)

    if 'simulation_folder' not in input_params or not input_params['simulation_folder']:
        if 'simulation_id' not in input_params or not input_params['simulation_id']:
            simulation_id = 'pmv_comfort_map_%d' % int(round(time.time(), 2) * 100)
        else:
            simulation_id = input_params['simulation_id']

        simulation_folder = os.path.join(project_folder, simulation_id)
        input_params['simulation_folder'] = simulation_folder
    else:
        simulation_folder = input_params['simulation_folder']

    # copy project folder content to simulation folder
    artifacts = ['ddy', 'epw', 'model']
    for artifact in artifacts:
        from_ = os.path.join(project_folder, input_params[artifact])
        to_ = os.path.join(simulation_folder, input_params[artifact])
        _copy_artifacts(from_, to_)

    luigi.build(
        [LetPmvComfortMapFly(_input_params=input_params)],
        local_scheduler=local_scheduler(),
        workers=workers
    )



if __name__ == '__main__':
    project_folder, user_values, workers = parse_input_args(sys.argv)
    start(project_folder, user_values, workers)
