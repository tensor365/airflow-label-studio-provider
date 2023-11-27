import time
from typing import Any, Callable, Dict, Optional

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook
from airflow.providers.label_studio.hooks.label_studio_hook import LabelStudioHook


class SyncTask(BaseOperator):
    """
    Trigger a Sync Task in Label Studio.

    :conn_id: connection to run the operator with it
    :idTask: str
    :idProject: str 
    :syncType: str

    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['id_task']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#e5e7eb'

    @apply_defaults
    def __init__(self, *, idTask: str = None , idProject: str= None, syncType: str =None ,conn_id: str = 'label_studio_conn_sample', **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.log.info(BaseHook.get_connection(self.conn_id))
        self.conn_type = BaseHook.get_connection(self.conn_id).conn_type
        self.idTask = idTask
        self.idProject = idProject
        self.syncType = syncType

    def on_kill(self):
        self.log.info("Initiate Label Studio Hook")
        hook = LabelStudioHook(conn_id=self.conn_id)

        self.log.info("Call HTTP method to kill task with id {}".format(self.idTask))
        response = hook.stopTask(taskId=self.idTask)

        if response.status_code == 200:
            self.log.info('Label Studio Sync Task {taskId} has been killed sucessfully'.format(taskId=self.idTask))
        return response

    def execute(self, context: Dict[str, Any]) -> Any:

        self.log.info("Initiate Label Studio Hook")
        hook = LabelStudioHook(conn_id=self.conn_id)

        self.log.info("Call HTTP method to reload task with id {}".format(self.idTask))
        response = hook.syncTask(idTask=self.idTask, idProject=self.idProject, syncType=self.syncType)
                
        if response.status_code not in range(200,300):
            raise ValueError('Error when launching Sync Task from Label Studio: {error}'.format(error=response.text))
      
        self.log.info('Status Code Return {}'.format(response.status_code))
        self.log.info('Answer Return {}'.format(response.text))

        return response.text