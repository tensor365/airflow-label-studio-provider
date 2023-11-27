<p align="center" style="vertical-align:center;">
  <a href="https://labelstud.io/">
    <img alt="Label Studio" src="" width="80", height="80" />
  </a>
</p>

<h1 align="center">
  Airflow: Label Studio (BETA)
</h1>
  <h3 align="center">
    Label Studio Provider to perform actions from Airflow.
</h3>

<br/>

This repository provides basic Label Studio hooks and operators to trigger tasks available in a Label Studio Site.

## Requirements

The package has been tested with Python 3.7, Python 3.8.

|  Package  |  Version  |
|-----------|-----------|
| apache-airflow | >2.0 |


## How to install it ?


To install it, download and unzip source and launch the following pip install command: 

```bash
pip install .
```

You can also use 

```bash
python setup.py install
```

## How to use it ?
<br/>


<br/>

### 1. Authentification Example
<br/>

**Prerequisites**:  
<br>
• A Label Studio Token
• URL of your Label Studio Site

**Step 1**: Login in your Airflow Server. 

**Step 2**: Go into Admin > Connections > Add A New Record. 

**Step 3**: Select Label Studio.

**Step 4** Provide following informations:

**Step 5** Save and your connection to Label Studio auth is ready to use !

### 4. Example: Creating a DAG with Label Studio Sync Operator to reload App 

You can now use the operators in your dags to trigger a reload of an app in Qlik Sense from Airflow

Example: 

```python

from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

from airflow.providers.label_studio.operators.sync_operator import SyncTask


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

idApp="" #Fill the id of your application you want to reload
connId="" #Fill the connection id you gave when creating the connection in airflow

with DAG(
    'LabelStudioSyncTask',
    default_args=default_args,
    description='A simple tutorial DAG reloading Label Studio Sync Task',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['Label Studio', 'Example'],
) as dag:
    
    op = SyncTask(app_id=idApp, conn_id=connId, task_id="QlikReloadTask")
    
    op

```

<br/>


