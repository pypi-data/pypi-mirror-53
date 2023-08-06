import base64
import json

import numpy as np

from .query_result import IdsQR, IdsScoresQR

def keyword_row_parser(row):
    ids_bytes = row.cells.get('i').get('i'.encode())[0].value
    ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
    return IdsQR().fromIds(ids)

def integer_row_parser(row):
    ids_bytes = row.cells.get('i').get('i'.encode())[0].value
    ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
    scores_bytes = row.cells.get('s').get('i'.encode())[0].value
    scores = np.array(np.frombuffer(scores_bytes, dtype=np.float32), dtype=np.float32)
    return IdsScoresQR(ids, scores)

def float_row_parser(row):
    ids_bytes = row.cells.get('i').get('i'.encode())[0].value
    ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
    scores_bytes = row.cells.get('s').get('f'.encode())[0].value
    scores = np.array(np.frombuffer(scores_bytes, dtype=np.float32), dtype=np.float32)
    return IdsScoresQR(ids, scores)

def doc_row_parser(row):
    response = row.cells.get('doc').get('doc'.encode())[0].value
    try:
        return json.loads(response)
    except:
        return response

row_parsers = {
    'keyword': keyword_row_parser,
    'text': keyword_row_parser,
    'integer': integer_row_parser,
    'float': float_row_parser,
    'doc': doc_row_parser
}


def keyword_row_key_formatter(field, value):
    encoded_value = base64.b64encode(value.encode()).decode('utf-8')
    row_key = '%s|%s' % (field, encoded_value)
    return row_key

def integer_row_key_formatter(field, value):
    return field

def float_row_key_formatter(field, value):
    return field

def boolean_row_key_formatter(field, value):
    if type(value) is str:
        return '%s|%s' % (field, value)
    else:
        return '%s|%s' % (field, 'true' if value else 'false')

def doc_row_key_formatter(doc_id, _):
    return 'doc|%s' % (doc_id)

row_key_formatters = {
    'keyword': keyword_row_key_formatter,
    'text': keyword_row_key_formatter,
    'integer': integer_row_key_formatter,
    'float': float_row_key_formatter,
    'boolean': boolean_row_key_formatter,
    'doc': doc_row_key_formatter
}