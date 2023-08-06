"""
  storage.py
  Copyright (c) Andreas Palsson and individual contributors.
  Licensed under the 3-clause BSD license.
"""
import os
from datetime import datetime, timezone
from typing import IO, AnyStr, Tuple, List, NamedTuple
from urllib.parse import urljoin, urlparse
from dateutil.parser import parse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.utils import timezone as tz
from django.utils.deconstruct import deconstructible
from lxml import etree as et
from lxml.etree import Element
from requests import Response, Session


class StorageItem(NamedTuple):
    name: str
    path: bool
    size: int
    created: datetime
    modified: datetime


@deconstructible
class WebDavStorage(Storage):
    def __init__(self, **settings):
        self.webdav_url = self._setting('STORAGE_WEBDAV_URL', '')
        self.webdav_username = self._setting('STORAGE_WEBDAV_USERNAME', '')
        self.webdav_password = self._setting('STORAGE_WEBDAV_PASSWORD', '')
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)
        self.use_tz = settings.get('USE_TZ', False)
        if not self.webdav_url:
            raise ImproperlyConfigured('The STORAGE_WEBDAV_URL setting is required')

    @staticmethod
    def _setting(name: str, default=None) -> str:
        return getattr(settings, name, default)

    @property
    def _session(self):
        if not hasattr(self, '_requests_session'):
            self._requests_session = Session()
        return self._requests_session

    def _propfind(self, path: str, depth: int = 1) -> Response:
        headers = {'Content-Type': 'text/xml', 'Depth': str(depth)}
        url = urljoin(self.webdav_url, path) if path else self.webdav_url
        data = '<?xml version="1.0" ?><D:propfind xmlns:D="DAV:"><D:allprop/></D:propfind>'
        return self._session.request('PROPFIND', url, data=data, headers=headers)

    def _parse_propfind(self, response: Response, path: str) -> List[StorageItem]:
        path = urlparse(urljoin(self.webdav_url, path) if path else self.webdav_url).path
        result: List[StorageItem] = list()
        root: Element = et.fromstring(response.content)
        responses = root.xpath("/*[local-name()='multistatus']/*[local-name()='response']")
        for response in responses:
            name: str = response.xpath("./*[local-name()='href']/text()")
            if len(name) == 1:
                name = name[0]
            collection = response.xpath(
                "./*[local-name()='propstat']/*[local-name()='prop']/*[local-name()='resourcetype']/*[local-name()='collection']")
            collection = bool(collection)
            length = response.xpath(
                "./*[local-name()='propstat']/*[local-name()='prop']/*[local-name()='getcontentlength']/text()")
            length = str(length[0]) if length else 0
            created = response.xpath(
                "./*[local-name()='propstat']/*[local-name()='prop']/*[local-name()='creationdate']/text()")
            created = parse(created.pop()) if created else datetime.fromtimestamp(0, timezone.utc)
            modified = response.xpath(
                "./*[local-name()='propstat']/*[local-name()='prop']/*[local-name()='getlastmodified']/text()")
            modified = parse(modified.pop()) if modified else datetime.fromtimestamp(0, timezone.utc)
            if name == path:  # if directory itself, set name to '.'
                name = '.'
            if name.startswith(path):
                name = name[len(path):]
            if name.endswith('/'):
                name = name[:-1]
            result.append(StorageItem(name, collection, length, created, modified))
        return result

    def _open(self, name: str, mode: str = 'rb') -> IO[AnyStr]:
        response = self._session.get(urljoin(self.webdav_url, name), stream=True)
        if response.ok:
            return response.raw
        raise FileNotFoundError('No such file or directory: {}'.format(name))

    def _save(self, name: str, content: IO[AnyStr]) -> str:
        paths = name.split(os.sep)
        filename = paths.pop()
        url = self.webdav_url
        for path in paths:
            url = urljoin(url + '/', path)
            self._session.request('MKCOL', url)
        url = urljoin(url + '/', filename)
        response: Response = self._session.put(url, data=content)
        if response.ok:
            return name
        raise IOError('Failed to save file: {} ({}) '.format(name, response.text))

    def delete(self, name: str) -> None:
        self._session.delete(urljoin(self.webdav_url, name))

    def exists(self, name: str) -> bool:
        headers = {'Content-Type': 'text/xml', 'Depth': '1'}
        url = urljoin(self.webdav_url, name)
        data = '<?xml version="1.0" ?><D:propfind xmlns:D="DAV:"><D:allprop/></D:propfind>'
        rv = self._session.request('PROPFIND', url, data=data, headers=headers)
        return rv.ok

    def listdir(self, path: str) -> Tuple[List[str], List[str]]:
        rv = self._propfind(path)
        if not rv.ok:
            return list(), list()
        items = self._parse_propfind(rv, path)
        return [i.name for i in items if i.path], [i.name for i in items if not i.path]

    def size(self, name: str):
        rv = self._propfind(name, 0)
        if rv.ok:
            items = self._parse_propfind(rv, name)
            if items:
                return int(items.pop().size)
        raise IOError('Could not get size for {}'.format(name))

    def url(self, name: str):
        return urljoin(self.webdav_url, name)

    def get_accessed_time(self, name):
        raise NotImplementedError('get_accessed_time() is not supported')

    def _get_time(self, name):
        rv = self._propfind(name, 0)
        if rv.ok:
            items = self._parse_propfind(rv, name)
            if items:
                return items.pop()
        return None

    def get_created_time(self, name):
        si = self._get_time(name)
        if si and si.created:
            if self.use_tz:
                return si.created
            return tz.localtime(si.created)
        raise NotImplementedError('get_created_time() is not supported')

    def get_modified_time(self, name):
        si = self._get_time(name)
        if si and si.modified:
            if self.use_tz:
                return si.modified
            return tz.localtime(si.modified)
        raise NotImplementedError('get_modified_time() is not supported')


class StaticWebDavStorage(WebDavStorage):
    @staticmethod
    def _setting(name: str, default=None) -> str:
        return getattr(settings, 'STATICFILES_' + name, default)
