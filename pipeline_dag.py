from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'MLOPS_pipeline',
    default_args=default_args,
    description='Automated pipeline with model training',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task 0: Delete unnecessary files
    delete_files = BashOperator(
        task_id='delete_files',
        bash_command='cd /opt/airflow/project && python delete_files.py'
    )

    # Task 1: Generate Data
    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='cd /opt/airflow/project && python LiveData.py'
    )

    # Task 2: Process Data
    process_data = BashOperator(
        task_id='process_data',
        bash_command='cd /opt/airflow/project && python EDA.py'
    )

    # Task 3: Train Model
    train_model = BashOperator(
        task_id='train_model',
        bash_command='cd /opt/airflow/project && python Model.py'
    )

    # Task 4: Upload Files to Google Drive
    upload_to_drive = BashOperator(
        task_id='upload_to_drive',
        bash_command='cd /opt/airflow/project && python Push.py'
    )

    # Define task dependencies
    delete_files >> generate_data >> process_data >> train_model >> upload_to_drive
