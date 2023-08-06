# sickdb-python 

A lightweight api wrapper for [`sickdb-api`](https://github.com/gltd/sickdb-api)


# installation 

```
pip3 install sickdb-client
```


# usage 
see [demo](examples/demo.py)

```python
import os
from sickdb_client import API

FIXTURE1 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'space-time-motion.mp3'))
FIXTURE2 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'space-time-motion.mp3'))


print("\nCONNECT TO THE API...\n")
api = API(url="http://localhost:3030/", api_key="dev", debug=True)

print("\nGETTING YOUR USER PROFILE...\n")
r = api.users.me()
print(r.json())
```
