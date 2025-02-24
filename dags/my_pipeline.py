"""
airflow webserver => localhost:8080
airflow scheduler
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


# Define common arguments
default_args = {
    "owner": "vmphat",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


# Define the DAG
with DAG(
    dag_id="dag_my_data_pipeline_v008",
    default_args=default_args,
    start_date=datetime(year=2025, month=2, day=22),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Define the tasks
    task_1 = BashOperator(
        task_id="crawl_tiktok_data",
        bash_command="cd /mnt/d/__AoIDA-Project && python src/crawler/crawler.py",
    )
    task_2 = BashOperator(
        task_id="extract_audio",
        bash_command="cd /mnt/d/__AoIDA-Project && python src/preprocess/extract_audio.py",
    )
    task_3 = BashOperator(
        task_id="audio_to_text",
        bash_command="cd /mnt/d/__AoIDA-Project && python src/preprocess/audio_to_text.py",
    )
    task_4 = BashOperator(
        task_id="flatten_merge_data",
        bash_command="cd /mnt/d/__AoIDA-Project && python src/preprocess/flatten_merge_data.py",
    )

    # Define the task dependencies
    task_1 >> task_2 >> task_3 >> task_4
