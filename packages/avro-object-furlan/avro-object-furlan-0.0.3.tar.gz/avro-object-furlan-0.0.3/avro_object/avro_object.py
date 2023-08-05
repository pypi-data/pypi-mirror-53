import datetime
import io
import json
import os

from fastavro import (is_avro, json_writer, parse_schema, reader, validate,
                      writer)

from .avro_tools import AvroTools

_json_fetch_modes = []


class AvroObject:
    """
    Helper class for AVRO objects

    :param data: (un)serialized data
    :param schema: Avro schema
    :type data: JSON as string, Dict object, Filename/URL as string with JSON content, Avro as bytes with binary serialized content
    :type schema: JSON as string, Dict object, Filename/URL as string with JSON content

    """

    def __init__(self, data, schema=None):
        """
        :param data: dict, list of dicts, JSON str, file, bytes
        :param schema: dict 
        """
        self._last_error = None     # Last error captured
        self._object_data = None
        self._json_data = None
        self._avro_data = None
        self._origin = None
        self._schema = None
        self._schema_origin = None

        self._ok = False
        if schema is None:
            self._schema = None
        elif isinstance(schema, str):
            try:
                success, schema, origin = AvroTools.fetch_json(schema)
                if success:
                    schema = json.loads(schema)
                    self._schema_origin = origin
                else:
                    schema = None

            except Exception as e:
                self._last_error = str(e)
                schema = None

        if schema is not None:
            self._schema = parse_schema(schema)
            if self._schema_origin is None:
                self._schema_origin = type(schema).__name__

        if isinstance(data, bytes):
            b_avro = False
            try:
                bdata = io.BytesIO(data)
                if is_avro(bdata):
                    self._origin = 'binary_avro'
                    bdata.seek(0)
                    b_avro = True
                    avro_reader = reader(bdata)
                    self._schema = avro_reader.schema
                    obj_data = []
                    for record in avro_reader:
                        obj_data.append(record)
                    self._object_data = None if len(obj_data) == 0 else obj_data[0] if len(
                        obj_data) == 1 else obj_data
                    self._ok = True
                else:
                    self._origin = 'binary_string'
                    data = data.decode('utf-8')

            except Exception as e:
                self._last_error = (
                    'Avro binary' if b_avro else 'String decoding')+f' error: {e}'

        if isinstance(data, str):
            success, json_data, origin = AvroTools.fetch_json(data)
            if not self._origin:
                self._origin = origin
            if not success:
                self._last_error = json_data
                return

            try:
                self._object_data = json.loads(json_data)
                self._json_data = json_data
                if self._schema is None:
                    self._ok = True
            except Exception as e:
                self._last_error = f'JSON parsing error: {e}'

        elif isinstance(data, dict) or isinstance(data, list):
            self._origin = type(data).__name__
            self._object_data = data
            if self._schema is None:
                self._ok = True

        if self._object_data is not None and not self._ok and self._schema is not None:
            try:
                validate(self._object_data, self._schema)
                self._ok = True
            except Exception as e:
                self._last_error = f'Schema error: {e}'

    def __str__(self):
        return f'{self._origin}:{self.to_json()}' + (f'[!{self._last_error}]' if self.last_error else '')

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        """    
        :return: JSON serialized data
        :rtype: str
        """
        if not self._ok or self._json_data:
            return self._json_data

        if self._schema is None:
            try:
                self._json_data = json.dumps(
                    self._object_data, default=AvroTools._json_converter)
            except Exception as e:
                self._last_error = f'JSON serialization error: {e}'
        else:
            out = io.StringIO()
            json_writer(out, self._schema, self._object_data if isinstance(
                self._object_data, list) else [self._object_data])
            out.flush()
            out.seek(0)
            self._json_data = out.read()

        return self._json_data

    def to_avro(self):
        """
        :return: AVRO bytes serialized data (when schema is informed) 
        :rtype: bytes
        """
        if not self._ok or self._avro_data or not self._schema:
            return self._avro_data

        out = io.BytesIO()
        writer(out, self._schema, self._object_data if isinstance(
            self._object_data, list) else [self._object_data])
        out.flush()
        out.seek(0)
        self._avro_data = out.read()
        return self._avro_data

    @property
    def json(self):
        """
        :return: JSON serialized data
        :rtype: str        
        """
        return self._json_data

    @property
    def data(self):
        """        
        :return: Native unserialized data
        :rtype: dict
        """
        return self._object_data

    @property
    def origin(self):
        """
        :return: Source of data (str, file, URL, Avro binary)
        :rtype: str
        """
        return self._origin

    @property
    def schema_origin(self):
        """
        :return: Source of schema (str, file, URL)
        :rtype: str
        """
        return self._schema_origin

    @property
    def ok(self):
        """
        :return: Avro Object successfull creation
        :rtype: bool
        """
        return self._ok

    @property
    def last_error(self):
        """
        :return: Last error message
        :rtype: str
        """
        return self._last_error
