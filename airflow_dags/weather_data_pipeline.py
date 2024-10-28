from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from job_scripts.data_extraction import fetch_weather_data
from job_scripts.data_transformation import transform_weather_data
from job_scripts.data_loading import load_data_to_s3, load_data_to_rds


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['your_email@example.com'],
    'start_date': days_ago(1),
}

with DAG('weather_data_pipeline', default_args=default_args, schedule_interval='@daily') as dag:

    def extract_data(**context):
        cities = ["Paris", "London", "New York"]
        raw_data = fetch_weather_data(cities)
        return raw_data

    def transform_data(**context):
        raw_data = context['task_instance'].xcom_pull(task_ids='extract_data')
        transformed_data = transform_weather_data(raw_data)
        return transformed_data

    def load_data_to_destinations(**context):
        transformed_data = context['task_instance'].xcom_pull(task_ids='transform_data')
        load_data_to_s3(transformed_data, "multiple_cities")
        load_data_to_rds(transformed_data)

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data_to_destinations,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
