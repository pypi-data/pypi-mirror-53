import datetime
import json
import numbers
import os
import re
from inspect import signature

import requests


class AvroTools:
    """
    Tools for AvroObject
    """
    _json_fetch_modes = []

    @classmethod
    def fetch_json(cls, source: str) -> tuple:
        '''Load JSON string from various medium and returns as string

        :param source: string JSON, file name, URL, another registered source by add_fetch_method
        :rtype: tuple (bool Success, str JSON or error message, origin)
        '''
        try:
            for method in cls._json_fetch_modes:
                success, message, origin = method(source)
                if success:
                    break
                else:
                    origin = "string"

            # Try to parse JSON str
            json.loads(message if success else source)
            return True, (message if success else source), origin
        except Exception as e:
            return False, str(e), None

    @classmethod
    def reset_fetch_methods(cls):
        """
        Resets default fetch methods (File, URL and string)
        """
        cls._json_fetch_modes.clear()
        for method in [AvroTools.fetch_json_file, AvroTools.fetch_json_url]:
            cls._json_fetch_modes.append(method)

    @classmethod
    def add_fetch_method(cls, method) -> bool:
        """
        Add custom fetch method

        :param method: (str source) -> (bool Success, str JSON/Error, str origin name)
        :return: Success
        :rtype: bool
        """
        try:
            sign = signature(method)
            if len(sign.parameters) != 1:
                return False
            if not (sign.return_annotation is tuple):
                return False
            if method not in cls._json_fetch_modes:
                cls._json_fetch_modes.append(method)
            return True
        except:
            pass
        return False

    @staticmethod
    def fetch_json_file(source: str) -> tuple:
        """Try to parse json from file

        :param source: str with file name
        :return: (bool Success, str JSON or Error, origin)
        """
        if os.path.isfile(source):
            try:
                with open(source, 'r') as f:
                    content = f.read()
                return True, content, f"file://{source}"
            except Exception as e:
                return False, str(e)
        else:
            return False, f"File not found: {source}", f"file://{source}"

    @staticmethod
    def fetch_json_url(source: str) -> tuple:
        """Try to parse json from url

        :param source: str with URL
        :return: (bool Success, str JSON or Error, origin)
        """

        pattern = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        if pattern.fullmatch(source):
            try:
                content = requests.get(url=source).text
                return True, content, source
            except Exception as e:
                return False, str(e)
        else:
            return False, f"Source is not an URL: {source}", source

    @staticmethod
    def _json_converter(o):
        """
        Default JSON serializer for datetime
        """
        for t in [datetime.time, datetime.date, datetime]:
            if isinstance(o, t):
                return o.__str__()
        return None

    @staticmethod
    def create_schema(data: dict, name: str, namespace: str = 'namespace.test', doc: str = None):
        '''
        Create schema from object (incomplete)

        :param data: source object
        :param name: Name of schema
        :param namespace: Namespace of schema
        :param doc: Documentation
        :return: Schema
        :rtype: dict
        '''
        if not isinstance(data, dict):
            return None
        schema = {
            'doc': 'A weather reading.',
            'name': 'Weather',
            'namespace': 'test',
            'type': 'record',
            'fields': [
                    {'name': 'station', 'type': 'string'},
                    {'name': 'time', 'type': 'long'},
                    {'name': 'temp', 'type': 'int'},
            ],
        }

        o_type = None
        if isinstance(data, dict):
            o_type = 'record'
        elif isinstance(data, list):
            o_type = 'array'
        elif isinstance(data, str):
            o_type = 'string'
        elif isinstance(data, numbers.Integral):
            o_type = 'int'
        elif isinstance(data, numbers.Real):
            o_type = 'float'
        else:
            return None
        if not name:
            return None
        schema = {
            'namespace': namespace,
            'type': o_type,
            'name': name,
            'fields': []
        }
        if isinstance(doc, str) and len(doc) > 0:
            schema['doc'] = doc

        for k, v in data.items():
            field = AvroTools.create_schema(data=v, name=k)
            schema['fields'].append(field)

        return schema
