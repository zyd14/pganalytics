"""

Project: pgbadger_container

File Name: get_log_files

Author: Zachary Romer, zach@scharp.org

Creation Date: 7/8/19

Version: 1.0

Purpose:

Special Notes:

"""

import boto3
import os

client = boto3.client('rds')


def get_logs(db_instance_id: str='') -> dict:
    if db_instance_id:
        rds_instances = (db_instance for db_instance in
                         client.describe_db_instances(DBInstanceIdentifier=db_instance_id)['DBInstances']['DBInstanceIdentifier'])
    rds_instances = (db_instance for db_instance in client.describe_db_instances()['DBInstances']['DBInstanceIdentifier'])
    log_refs = {}
    for r in rds_instances:
        if r not in log_refs:
            log_refs[r] = []
        log_refs[r].append([log_file for log_file in client.describe_db_log_files(DBInstanceIdentifier=r)])
    return log_refs


def download_logs(log_refs: dict):
    pgbadger_dir = os.getenv('PGBADGER_DATA')
    for instance, logs in log_refs.items():
        for log_file in logs:
            log_file_data = client.download_db_log_file_portion(DBInstanceIdentifier=instance, LogFileName=log_file)
            with open(f'{pgbadger_dir}/{log_file}.log', 'w') as log_file_write:
                log_file_write.writelines(log_file_data)


def run_pgbadger():
    os.system('pgbadger')


if __name__ == '__main__':
    log_refs = get_logs()
    download_logs(log_refs)
    run_pgbadger()
