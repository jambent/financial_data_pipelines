from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
import boto3
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5)
}

dg = DAG('FX_s3_sensor',
          schedule_interval='/10 * * * *',
          default_args=default_args,
          catchup=False
          )

s3_client = boto3.client('s3')

buckets = s3_client.list_buckets()
bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]

matched_bucket_name = [match for match in bucket_names if "landing" in match]
s3_bucket_name = matched_bucket_name[0]

s3_key = 'test.txt'

s3_sensor = S3KeySensor(
    task_id='s3_FX_file_check',
    poke_interval=60,
    timeout=180,
    soft_fail=False,
    retries=2,
    bucket_key=s3_key,
    bucket_name=s3_bucket_name,
    aws_conn_id='aws_default',
    dag=dg)


def processing_func(**kwargs):
    print("Reading the file")
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=s3_bucket_name, Key=s3_key)
    lin = obj['Body'].read().decode("utf-8")
    print(lin)


func_task = PythonOperator(
    task_id='a_task_using_fx_file',
    python_callable=processing_func,
    dag=dg)

s3_sensor >> func_task