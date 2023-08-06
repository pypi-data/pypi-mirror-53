<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-traceback.svg?longCache=True)](https://pypi.org/project/django-traceback/)

#### Installation
```bash
$ [sudo] pip install django-traceback
```

#### Models
model|`__doc__`
-|-
`Traceback` |Traceback(id, type, value, traceback, path, created_at)

#### Functions
function|`__doc__`
-|-
`django_traceback.utils.save_traceback(path=None)` |save a traceback

#### Examples
```python
from django_traceback.utils import save_traceback
import requests
from apps.celery import celery_app

@celery_app.task
def task():
    try:
        r = requests.get('url')
    except (requests.exceptions.ConnectionError,...):
        save_traceback(__file__)
        # init task again
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>