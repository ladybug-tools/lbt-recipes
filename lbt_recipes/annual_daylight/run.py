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


import sys
import luigi
import os
import time
import pathlib
from multiprocessing import freeze_support
from queenbee_local import local_scheduler, _copy_artifacts, update_params, parse_input_args, LOGS_CONFIG

import flow.main as annual_daylight_workerbee


_recipe_default_inputs = {   'grid_filter': '*',
    'model': None,
    'north': 0.0,
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'schedule': None,
    'sensor_count': 200,
    'thresholds': '-t 300 -lt 100 -ut 3000',
    'wea': None}


class LetAnnualDaylightFly(luigi.WrapperTask):
    # global parameters
    _input_params = luigi.DictParameter()

    def requires(self):
        yield [annual_daylight_workerbee._Main_eb7c12e7Orchestrator(_input_params=self._input_params)]


def start(project_folder, user_values, workers):
    freeze_support()

    input_params = update_params(_recipe_default_inputs, user_values)

    if 'simulation_folder' not in input_params or not input_params['simulation_folder']:
        if 'simulation_id' not in input_params or not input_params['simulation_id']:
            simulation_id = 'annual_daylight_%d' % int(round(time.time(), 2) * 100)
        else:
            simulation_id = input_params['simulation_id']

        simulation_folder = os.path.join(project_folder, simulation_id)
        input_params['simulation_folder'] = simulation_folder
    else:
        simulation_folder = input_params['simulation_folder']

    # copy project folder content to simulation folder
    artifacts = ['model', 'schedule', 'wea']
    optional_artifacts = ['schedule']
    for artifact in artifacts:
        value = input_params[artifact]
        if value is None:
            if artifact in optional_artifacts:
                continue
            raise ValueError('None value for required artifact input: %s' % artifact)
        from_ = os.path.join(project_folder, input_params[artifact])
        to_ = os.path.join(simulation_folder, input_params[artifact])
        _copy_artifacts(from_, to_)

    # set up logs
    log_folder = pathlib.Path(simulation_folder, '__logs__')
    log_folder.mkdir(exist_ok=True)
    cfg_file = pathlib.Path(simulation_folder, '__logs__', 'logs.cfg')
    log_file = pathlib.Path(simulation_folder, '__logs__', 'logs.log').as_posix()
    with cfg_file.open('w') as lf:
        lf.write(LOGS_CONFIG.replace('WORKFLOW.LOG', log_file))

    luigi.build(
        [LetAnnualDaylightFly(_input_params=input_params)],
        local_scheduler=local_scheduler(),
        workers=workers,
        logging_conf_file=cfg_file.as_posix()
    )


if __name__ == '__main__':
    project_folder, user_values, workers = parse_input_args(sys.argv)
    start(project_folder, user_values, workers)
