#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import yaml
import subprocess
import click


@click.group()
@click.pass_context
def main(ctx):
    WAVES_URL = os.environ.get('WAVES_URL')

    if not WAVES_URL:
        click.secho('set the WAVES_URL environment variable.', fg='red')
        ctx.exit(-1)

    ctx.obj['config'] = {
        'WAVES_URL': WAVES_URL,
    }


@main.command(name='register-business-task')
@click.argument('yaml_filepath', required=True, type=click.File('rb'))
@click.option('--name', required=True, help='aweeds')
@click.option('--version', required=False, default='latest')
@click.pass_context
def register_business_task(ctx, yaml_filepath, name, version):
    """
    Register the business task
    """
    definition = yaml.load(yaml_filepath, Loader=yaml.FullLoader)

    # new_product = ctx.obj.client.create_product(name, description, labels, options,
    #                                            batch_timeout=batch_timeout, skip_reasons=skip_reason)

    # click.secho(json.dumps(new_product, indent=2, sort_keys=True), fg='green')
    click.secho("   ...Publishing {}@{}".format(name, version), fg='yellow')
    click.secho(json.dumps(definition, indent=2, sort_keys=True), fg='green')


@main.command(name='start-worker')
@click.argument('yaml_filepath', required=True, type=click.File('rb'))
@click.option('--tasks', required=False, help='The path for the business task tasks.py file')
@click.pass_context
def start_worker(ctx, yaml_filepath, tasks):
    """
    Start receiving messages for current bt
    """
    definition = yaml.load(yaml_filepath, Loader=yaml.FullLoader)

    task_name = definition.get('business_task')
    task_version = definition.get('version', 'latest')
    tasks_module = definition.get('tasks_module', 'waves.tasks.app')
    if tasks:
        tasks_module = tasks
    default_queue = '{}_{}'.format(task_name, task_version)
    loglevel = 'INFO'

    concurrency = os.environ.get('CELERY_CONCURRENCY', 1)
    queue = os.environ.get('QUEUE_NAME', default_queue)
    worker_name = os.environ.get('WORKER_HOSTNAME', 'worker')

    # --detach
    cmd = 'celery -A {} worker --hostname {}@{} --loglevel={} --task-events -Ofair -c {} -Q {}'.format(
        tasks_module, task_name, worker_name, loglevel, concurrency, queue)
    click.secho("   ...Starting worker\n{}".format(cmd), fg='yellow')

    subprocess.Popen(cmd.split(' '))


@main.command(name='stop-worker')
@click.argument('yaml_filepath', required=True, type=click.File('rb'))
@click.option('--tasks', required=False, help='The path for the business task tasks.py file')
@click.pass_context
def stop_worker(ctx, yaml_filepath, tasks):
    """
    Start receiving messages for current bt
    """
    definition = yaml.load(yaml_filepath, Loader=yaml.FullLoader)
    tasks_module = definition.get('tasks_module', 'waves.tasks.app')

    if tasks:
        tasks_module = tasks

    cmd = 'celery -A {} control shutdown'.format(tasks_module)
    click.secho("   ...Stopping worker\n{}".format(cmd), fg='yellow')

    subprocess.Popen(cmd.split(' '))
