## Django Storage System for WebDAV

Django Storage System for WebDAV is a storage system for Django that allows
the user to use a WebDAV server as file storage for media files and also
static files.

This work is licensed under the 3-clause BSD license,
for more information see LICENSE.txt

### Prerequisites

Django v2.2 and Python v3.5 (or higher)

### Building and installing from source

To install the module in the current virtual environment.

    python3 setup.py clean --all install

To instead install in your home directory.

    python3 setup.py clean --all install --user

### Configuration Settings

Following parameters are used by the generic file storage system to
connect and authenticate against the WebDAV server.

    STORAGE_WEBDAV_URL = "https://www.example.org/media/"
    STORAGE_WEBDAV_USERNAME = "username"
    STORAGE_WEBDAV_PASSWORD = "password123"

To enable the storage system, see [Managing files](https://docs.djangoproject.com/en/2.2/topics/files/)
in the Django documentation.

In short; the actual configuration for the generic file storage is `DEFAULT_FILE_STORAGE`, i.e.

    DEFAULT_FILE_STORAGE = "django_storage_webdav.WebDavStorage"

To use the storage system for static files, use the following parameters.

    STATIC_STORAGE_WEBDAV_URL="https://www.example.org/static/"
    STATIC_STORAGE_WEBDAV_USERNAME="username"
    STATIC_STORAGE_WEBDAV_PASSWORD="password123"

And then activate the storage system by setting the `STATICFILES_STORAGE` parameter.

    STATICFILES_STORAGE = "django_storage_webdav.StaticWebDavStorage"

### Installation in local package index (e.g. DevPi) 

The commands below builds and install the artifacts in a local package index
(DevPi) at http://devpi.myserver.lan/ under the `staging` index. 

    python3 setup.py clean --all sdist bdist_wheel
    python3 -m pip install --upgrade twine
    python3 -m twine register --verbose --repository staging dist/*tar.gz
    python3 -m twine upload --repository-url http://devpi.myserver.lan/ --repository staging dist/*
