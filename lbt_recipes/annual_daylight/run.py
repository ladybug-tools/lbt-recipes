"""
This file is auto-generated from annual-daylight:0.10.20.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import sys
import datetime
import json
import luigi
import time
import pathlib
import shutil
from multiprocessing import freeze_support
from queenbee_local import local_scheduler, _copy_artifacts, update_params, parse_input_args, LOGS_CONFIG
from luigi.execution_summary import LuigiStatusCode

import flow.main_e6056798 as annual_daylight_workerbee


_recipe_default_inputs = {   'cpu_count': 50,
    'grid_filter': '*',
    'grid_metrics': None,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05 -dr 0',
    'schedule': None,
    'thresholds': '-t 300 -lt 100 -ut 3000',
    'timestep': 1,
    'wea': None}


class LetAnnualDaylightFly(luigi.WrapperTask):
    # global parameters
    _input_params = luigi.DictParameter()

    def requires(self):
        yield [annual_daylight_workerbee._Main_e6056798Orchestrator(_input_params=self._input_params)]


def start(project_folder, user_values, workers):
    freeze_support()

    input_params = update_params(_recipe_default_inputs, user_values)

    if 'simulation_folder' not in input_params or not input_params['simulation_folder']:
        if 'simulation_id' not in input_params or not input_params['simulation_id']:
            simulation_id = 'annual_daylight_%d' % int(round(time.time(), 2) * 100)
        else:
            simulation_id = input_params['simulation_id']

        simulation_folder = pathlib.Path(project_folder, simulation_id).as_posix()
        input_params['simulation_folder'] = simulation_folder
    else:
        simulation_folder = input_params['simulation_folder']

    # copy project folder content to simulation folder
    artifacts = ['grid_metrics', 'model', 'schedule', 'wea']
    optional_artifacts = ['grid_metrics', 'schedule']
    for artifact in artifacts:
        value = input_params[artifact]
        if value is None:
            if artifact in optional_artifacts:
                continue
            raise ValueError('None value for required artifact input: %s' % artifact)
        from_ = pathlib.Path(project_folder, input_params[artifact]).resolve().as_posix()
        to_ = pathlib.Path(simulation_folder, input_params[artifact]).resolve().as_posix()
        _copy_artifacts(from_, to_)
        # update the value to the new local value
        input_params[artifact] = to_

    # set up logs
    log_folder = pathlib.Path(simulation_folder, '__logs__')
    log_folder.mkdir(exist_ok=True)
    cfg_file = pathlib.Path(simulation_folder, '__logs__', 'logs.cfg')
    log_file = pathlib.Path(simulation_folder, '__logs__', 'logs.log').as_posix()
    err_file = pathlib.Path(simulation_folder, '__logs__', 'err.log').as_posix()
    with cfg_file.open('w') as lf:
        log_config_content = LOGS_CONFIG.replace('WORKFLOW.LOG', log_file).replace('ERROR.LOG', err_file)
        lf.write(log_config_content)

    status_file = log_folder.joinpath('status.json')
    if status_file.exists():
        status_file.unlink()
    shutil.copyfile(
        pathlib.Path(__file__).parent.joinpath('status.json'),
        status_file
    )

    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    status = json.loads(status_file.read_text())
    # update the input/output values in status
    for inp in status['status']['inputs']:
        try:
            value = input_params[inp['name'].replace('-', '_')]
        except KeyError:
            continue
        if 'source' in inp:
            inp['source']['path'] = value
        else:
            inp['value'] = value

    for out in status['status']['outputs']:
        if 'source' in out:
            value = pathlib.Path(simulation_folder, out['source']['path'])
            out['source']['path'] = value.as_posix()
        else:
            value = pathlib.Path(simulation_folder, out['path'])
            out['path'] = value.as_posix()
    status['status']['started_at'] = now
    status['status']['status'] = 'Running'
    status_file.write_text(json.dumps(status))

    summary = luigi.build(
        [LetAnnualDaylightFly(_input_params=input_params)],
        local_scheduler=local_scheduler(),
        workers=workers,
        detailed_summary=True,
        logging_conf_file=cfg_file.as_posix()
    )

    now = datetime.datetime.utcnow()
    try:
        status = json.loads(status_file.read_text())
    except json.JSONDecodeError:
        time.sleep(2)
        try:
            status = json.loads(status_file.read_text())
        except json.JSONDecodeError:
            # the status will be wrong
            print('Failed to read the latest status.')
            pass
    duration = now - datetime.datetime.strptime(
        status['status']['started_at'], '%Y-%m-%dT%H:%M:%SZ'
    )
    duration -= datetime.timedelta(microseconds=duration.microseconds)
    status['status']['finished_at'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    status['status']['status'] = 'Cancelled'
    status_file.write_text(json.dumps(status))
    if summary.status == LuigiStatusCode.FAILED:
        status['status']['status'] = 'Failed'
    elif summary.status == LuigiStatusCode.SUCCESS:
        status['status']['status'] = 'Succeeded'
    status['meta']['progress']['running'] = 0
    status['meta']['progress']['completed'] = status['meta']['progress']['total']
    status_file.write_text(json.dumps(status))

    cpu_usage = status['meta']['resources_duration']['cpu']

    print(summary.summary_text)

    print(f'Duration: {duration}    CPU Usage: {datetime.timedelta(seconds=cpu_usage)}')

    print(f'More info:\n - {log_file}\n - {err_file}')


if __name__ == '__main__':
    project_folder, user_values, workers = parse_input_args(sys.argv)
    start(project_folder, user_values, workers)
