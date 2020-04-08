import requests
from .rest_client import AttunityRestAPI

class Replicate(AttunityRestAPI):
	
	def tasks(self, server_name, **kwargs):
		url = f'/servers/{server_name}/tasks'
		tasks = self.request(path=url, method='GET')["taskList"]

		if "tags" in kwargs:
			tasks = [task for task in tasks if set(kwargs['tags']) & set(task['assigned_tags'])]

		if kwargs.get("running")==True:
			tasks = [task for task in tasks if task['state'] == 'RUNNING']

		return tasks

	def start_task(self, server_name, task_name, **kwargs):
		url = f'/servers/{server_name}/tasks/{task_name}?action=run&option=RESUME_PROCESSING'
		
		return self.request(path=url, method='POST')

	def stop_task(self, server_name, task_name, **kwargs):
		url = f'/servers/{server_name}/tasks/{task_name}?action=stop'
		headers = self._session.headers.update({ 
			'Content-Length': '0'
		})
		return self.request(path=url, method='POST', headers=headers)

	def get_task_details(self, server_name, task_name):
		url = f'/servers/{server_name}/tasks/{task_name}'
		
		return self.request(path=url, method='GET')
