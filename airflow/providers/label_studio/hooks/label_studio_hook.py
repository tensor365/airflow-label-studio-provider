from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator
import random
import string
import requests
import base64
import json

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

class LabelStudioHook(BaseHook):

    default_conn_name = 'label_studio_default'
    conn_type = "label_studio"
    hook_name = "Label Studio"
    base_url = None
    conn_name_attr='labe_studio_conn_id' 

    def __init__(self,conn_id: str = default_conn_name) -> None:
        self.conn_id = conn_id
        super().__init__()
    
    def test_connection(self):
        """

        Test the Label Studio connection by running a simple HTTP status.

        """

        try:
            self.get_status_api()
        except Exception as e:
            return False, str(e)
        return True, "Connection successfully tested" 
    
    def __convert_into_base64(self, body:str):
        """

        Method used to convert a body into base64 string

        """
        return base64.b64encode(json.dumps(body).encode('ascii')).decode('ascii')

        
    def ImportSyncTask(self, 
                idSyncTask:str = None, 
                idProject: str = None, 
                syncType: str = 'localfiles'
                ):
        """

        Synchronizing Import Task in Label Studio from a project

        """

        assert syncType in ['localfiles', 'azure', 'gcs', 's3']

        URI = f"/api/storages/{syncType}/{idSyncTask}/sync"
        
        body = {
                "project": idProject
                }

        ans = self.run(method='POST',endpoint=URI, body=body)
        return ans

    def ExportSyncTask(self, 
                idSyncTask:str = None, 
                idProject: str = None, 
                syncType: str = 'localfiles'
                ):
        """

        Synchronizing Export Task in Label Studio from a project

        """

        assert syncType in ['localfiles', 'azure', 'gcs', 's3']

        URI = f"/api/storages/export/{syncType}/{idSyncTask}/sync"
        
        body = {
                "project": idProject
                }

        ans = self.run(method='POST',endpoint=URI, body=body)
        return ans



    def get_conn(self) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        
        session = requests.Session()

        if self.conn_id:
            conn = self.get_connection(self.conn_id)
        host = conn.host if conn.host else ""

        if not host.startswith('https://') and not host.startswith('http://'):
            host = 'https://'+host
        self.base_url = host

        if conn.password != '':
            authHeaders = {
                "Authorization": f"Token {conn.password}"
            } 
            session.headers = authHeaders
        else: 
            raise RuntimeError('Please provide a Label Studio Token.')

        return session

    def run(
        self,
        method: str='GET',
        endpoint: Optional[str] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        **request_kwargs: Any,
    ) -> Any:
        r"""
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        self.session = self.get_conn()

        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')

        if method == 'GET':
            # GET uses params
            req = requests.Request(
                method, url, headers=headers)
        elif method=='POST':
            # Others use data
            import json
            req = requests.Request(
                method, url, data=json.dumps(data), headers=headers)
        else:
            raise RuntimeError('Method not handle by Label Studio Provider')

        self.log.info("Sending '%s' to url: %s", method, url)

        prepped = self.session.prepare_request(req)
        try:
            response = self.session.send(prepped, verify=False, allow_redirects=True)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning(
                '%s Tenacity will retry to execute the operation', ex)
            raise ex

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ['login','port', 'schema'],
            "relabeling": {
                'password': 'Label Studio Token'
            },
            "placeholders": {
                'host': 'URL to Label Studio',
                'password': 'Enter Label Studio Token',
            },
        }





