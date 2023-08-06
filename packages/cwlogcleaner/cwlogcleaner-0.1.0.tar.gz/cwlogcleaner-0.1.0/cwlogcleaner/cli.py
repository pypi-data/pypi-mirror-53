import logging
import inquirer
import boto3

from . import __version__

logger = logging.getLogger(__name__)


def main():
    logs = boto3.client('logs')

    groupNames = []

    paginator = logs.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        for group in page['logGroups']:
            groupNames.append(group['logGroupName'])

    questions = [
        inquirer.Checkbox('groups',
                          message="Which groups should be deleted?",
                          choices=groupNames,
                          ),
    ]
    answers = inquirer.prompt(questions)

    for group in answers['groups']:
        logger.info(f'Deleting group {group}')
        logs.delete_log_group(logGroupName=group)
