# pyplicate
A pythonic wrapper for Attunity Replicates REST API

# Examples
Authentication with the Replicate instance by specifying username, password and domain.

```python
from pyplicate import rest_client

api = rest_client.AttunityRestAPI(
	url='http://localhost:8000',
	username='admin',
	password='admin',
	domain='localdomain')
```

It also possible to authenticate by using the Baic token directly, as so:

```python
from pyplicate import rest_client

api = rest_client.AttunityRestAPI(
    url='http://localhost:8000',
    api_token='sOmeTh1nG_b4S3_64_3nc0d3d')
```

Example of how to receive all task that exists on a Replicate instance, and afterwards stopping all of them.
```python
from pyplicate import rest_client

api = rest_client.AttunityRestAPI(
    url='http://localhost:8090',
    api_token='sOmeTh1nG_b4S3_64_3nc0d3d')

tasks = Replicate.tasks(api, server_name='Replicate_server_name')

for task in tasks:
      Replicate.stop_task(api, server_name='Replicate_server_name', task_name=task["name"])
```





