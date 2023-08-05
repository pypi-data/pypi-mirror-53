__all__ = ['avro_object', 'avro_tools']

from .avro_object import AvroObject
from .avro_tools import AvroTools

name = 'avro_object'
version = '0.0.6'
description = 'Helper class for (de)serialization of objects using Apache Avro'
author = 'Guionardo Furlan'
author_email = 'guionardo@gmail.com'

AvroTools.reset_fetch_methods()
