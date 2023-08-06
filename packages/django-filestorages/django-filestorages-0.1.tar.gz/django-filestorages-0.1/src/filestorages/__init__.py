from django.conf import settings
from django.core.files.storage import default_storage, get_storage_class


def get_storage_def(name, up_options=None):
    conf = settings.FILE_STORAGES.get(name, {})

    options = conf.get('OPTIONS', {})
    if up_options:
        options.update(up_options)

    if 'BACKEND' in conf:
        return conf['BACKEND'], options

    parts = name.rsplit('.', 1)

    # If name is dotted path, go a level up.
    if len(parts) > 1:
        return get_storage_def(parts[0], options)

    # If no more dots, go for default.
    if name != 'default':
        return get_storage_def('default', options)

    # If we've reached the default, go for Django default.
    return settings.DEFAULT_FILE_STORAGE, options


def get_storage(name):
    if hasattr(settings, 'FILE_STORAGES'):
        backend, options = get_storage_def(name)
    else:
        backend, options = settings.DEFAULT_FILE_STORAGE, {}
    
    storage = get_storage_class(backend)(**options)

    storage.deconstruct = lambda: (
        "%s.get_storage" % get_storage.__module__,
        (name,), {}
    )

    return storage

