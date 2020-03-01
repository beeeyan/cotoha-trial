# -*- coding:utf-8 -*-

import json
import codecs
import marshmallow_dataclass
from respobj.coreference import Coreference

def json_to_coreference(jsonstr):
    json_formated = codecs.decode(json.dumps(jsonstr),'unicode-escape')
    result = marshmallow_dataclass.class_schema( Coreference )().loads(json_formated)
    return result
