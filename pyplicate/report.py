import requests
from .rest_client import AttunityRestAPI

class Report(AttunityRestAPI):

	def get_server_details(self, server_name, **kwargs):
		url = f'/servers/{server_name}'
		return self.request(path=url, method='GET')


