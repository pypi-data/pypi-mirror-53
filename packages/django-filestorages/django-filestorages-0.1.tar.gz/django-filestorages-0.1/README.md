# django-filestorages

Django-getstorage is a tiny Python library for dealing with configurable
Django storages.

It allows you to define a dictionary of file storage configurations
in your `settings` and refer to them by name in your code.

It should be obsolete once [Django ticket 26029](https://code.djangoproject.com/ticket/26029)
is resolved.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install django-filestorages.

```bash
pip install django-filestorages
```


## Usage

Wherever you need a storage, use the `filestorages.get_storage` function.

```python
from filestorages import get_storage

file = models.FileField(storage=get_storage('some.configured.storage'))
```


In your settings, you can define your storages using dotted paths:

```python
FILE_STORAGES = {
    'default': {
        'BACKEND': "django.core.files.storage.FileSystemStorage",
        'OPTIONS': {
            'location': '/path/to/the/files/',
            'base_url': '/files/',
        }
    },
    'some': {
        'BACKEND': 'other.backend.Storage',
        'OPTIONS': {
            'option': 'value',
        },
    },
    'some.configured': {
        'OPTIONS': {
            'second_option': True,
        },
    },
}
```

In this example `get_storage('some.configured.storage')` returns `other.backend.Storage(option='value', second_option=True)`

If no matching backend is found, `FILE_STORAGES['default']` is used, falling back on 
`DEFAULT_FILE_STORAGE` if not set.



## License
[MIT](https://choosealicense.com/licenses/mit/)
