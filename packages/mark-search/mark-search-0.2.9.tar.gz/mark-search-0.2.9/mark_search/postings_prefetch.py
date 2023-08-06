import base64
from google.cloud.bigtable import row_set

from .query_result import EmptyQR

from .row_parsers import row_parsers, row_key_formatters

from .query_validator import getTypeOfFieldFromMapping

from .analyzers import analyze_from_mapping


# ************ assume query has been validated ************ #



def boolTypesGetter(query, mapping):
    rkt = {}
    for key in query:
        rkt.update(row_key_type_getters[key](query[key], mapping))
    return rkt

def boolChildTypesGetter(query, mapping):
    rkt = {}
    for item in query:
        op = [k for k in item][0]
        rkt.update(row_key_type_getters[op](item[op], mapping))
    return rkt

def termTypesGetter(query, mapping):
    rkt = {}
    field = [k for k in query][0]
    value = query[field]['value']
    row_key = row_key_formatters['keyword'](field, value)
    rkt[row_key] = {
        'field': field,
        'type': 'keyword'
    }
    return rkt

def termsTypesGetter(query, mapping):
    rkt = {}
    field = [k for k in query][0]
    
    for value in query[field]:
        row_key = row_key_formatters['keyword'](field, value)
        rkt[row_key] = {
            'field': field,
            'type': 'keyword'
        }
    return rkt

def matchTypesGetter(query, mapping):
    rkt = {}
    field = [k for k in query][0]
    match_string = query[field]
    tokens = analyze_from_mapping(field, match_string, mapping, return_text=False)

    for value in tokens:
        row_key = row_key_formatters['keyword'](field, value)
        rkt[row_key] = {
            'field': field,
            'type': 'keyword'
        }
    return rkt

def rangeTypesGetter(query, mapping):
    rkt = {}
    field = [k for k in query][0]
    field_type = getTypeOfFieldFromMapping(field, mapping)
    row_key = row_key_formatters[field_type](field, None)
    rkt[row_key] = {
        'field': field,
        'type': field_type
    }
    return rkt

def fieldBoostTypesGetter(query, mapping):
    rkt = {}
    field = query['field']
    field_type = getTypeOfFieldFromMapping(field, mapping)
    row_key = row_key_formatters[field_type](field, None)
    rkt[row_key] = {
        'field': field,
        'type': field_type
    }
    return rkt

def scoredTermTypesGetter(query, mapping):
    rkt = {}
    field = query['field']
    value = query['value']
    field_type = getTypeOfFieldFromMapping(field, mapping)
    row_key = row_key_formatters[field_type](field, value)
    rkt[row_key] = {
        'field': field,
        'type': field_type
    }
    return rkt

row_key_type_getters = {
    'bool': boolTypesGetter,
    'filter': boolChildTypesGetter,
    'must': boolChildTypesGetter,
    'should': boolChildTypesGetter,
    'must_not': boolChildTypesGetter,
    'term': termTypesGetter,
    'terms': termsTypesGetter,
    'match': matchTypesGetter,
    'range': rangeTypesGetter,
    'fieldBoost': fieldBoostTypesGetter,
    'field_boost': fieldBoostTypesGetter,
    'scored_term': scoredTermTypesGetter
}

# given a query and an index mapping
# return a dictionary containing all the rowkeys
# the query needs and their types
def getRowKeysAndTypes(query, mapping):
    op = [k for k in query][0]
    row_keys_types = row_key_type_getters[op](query[op], mapping)
    return row_keys_types


# given a query and an index,
# efficiently fetch all the postings the query will need
# returns a dictionary of row_key to QueryResult
def prefetchPostings(query, index):
    row_keys_types = getRowKeysAndTypes(query, index.mapping)

    row_keys_types = {key: row_keys_types[key] for key in row_keys_types 
        if not index.has_row_key_cached(key, field=row_keys_types[key]['field'])}

    rs = row_set.RowSet()
    set_size = 0
    for rk in row_keys_types:
        rs.add_row_key(rk)
        set_size += 1
    if set_size > 0:
        partial_rows_data = index.bt_table.read_rows(row_set=rs, filter_=index.bt_row_filter)
        partial_rows_data.consume_all()

        for rk in row_keys_types:
            row = partial_rows_data.rows.get(rk.encode())
            t = row_keys_types[rk]['type']
            f = row_keys_types[rk]['field']
            qr = None
            if row is None:
                qr = EmptyQR()
            else:
                qr = row_parsers[t](row)
            
            if f in index.ttled_fields:
                index.ttl_cache[rk] = qr
            else:
                index.lru_cache[rk] = qr
        