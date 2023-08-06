numeric_field_types = {'integer', 'float'}
keyword_like_types = {'keyword', 'text', 'boolean'}

def getTypeOfFieldFromMapping(field, mapping):
    assert type(field) is str
    field_type = None
    spec = {}
    spec.update(mapping)
    for f in field.split('.'):
        spec = spec.get('properties', spec)
        spec = spec.get(f, {})
    field_type = spec.get('type')
    return field_type


def validateBool(query, mapping):
    assert type(query) is dict
    allowed_keys = {'must', 'should', 'filter', 'must_not'}
    for key in query:
        assert key in allowed_keys
        query_validators[key](query[key], mapping)
    return True

def validateFilter(query, mapping):
    assert type(query) is list
    for item in query:
        assert type(item) is dict
        assert len(item) == 1
        key = [k for k in item][0]
        query_validators[key](item[key], mapping)
    return True

def validateMustNot(query, mapping):
    assert type(query) is list
    for item in query:
        assert type(item) is dict
        assert len(item) == 1
        key = [k for k in item][0]
        query_validators[key](item[key], mapping)
    return True

def validateMust(query, mapping):
    assert type(query) is list
    for item in query:
        assert type(item) is dict
        assert len(item) == 1
        key = [k for k in item][0]
        query_validators[key](item[key], mapping)
    return True

def validateShould(query, mapping):
    assert type(query) is list
    for item in query:
        assert type(item) is dict
        assert len(item) == 1
        key = [k for k in item][0]
        query_validators[key](item[key], mapping)
    return True

def validateTerm(query, mapping):
    assert type(query) is dict
    assert len(query) == 1

    field = [k for k in query][0]
    field_type = getTypeOfFieldFromMapping(field, mapping)
    assert field_type is not None
    assert field_type in keyword_like_types

    assert 'value' in query[field]
    value = query[field].get('value')
    assert type(value) is str

    return True

def validateTerms(query, mapping):
    assert type(query) is dict
    assert len(query) == 1

    field = [k for k in query][0]
    field_type = getTypeOfFieldFromMapping(field, mapping)
    assert field_type is not None
    assert field_type in keyword_like_types

    value = query[field]

    assert type(value) is list and False not in [type(v) is str for v in value]

    return True

def validateMatch(query, mapping):
    assert type(query) is dict
    assert len(query) == 1

    field = [k for k in query][0]
    field_type = getTypeOfFieldFromMapping(field, mapping)
    assert field_type is not None
    assert field_type in keyword_like_types

    value = query[field]
    assert type(value) is str

    return True

def validateRange(query, mapping):
    assert type(query) is dict
    assert len(query) == 1

    field = [k for k in query][0]
    field_type = getTypeOfFieldFromMapping(field, mapping)
    assert field_type is not None
    assert field_type in numeric_field_types

    value = query[field]
    assert type(value) is dict
    assert len(value) > 0
    valid_bounds = {'gt', 'lt', 'gte', 'lte'}
    assert False not in [key in valid_bounds for key in value]
    assert False not in [type(value[key]) in {float, int} for key in value]

    return True

def validateFieldBoost(query, mapping):
    assert type(query) is dict
    
    allowed_fields = {'field', 'boost'}
    assert False not in [field in allowed_fields for field in query]

    assert 'field' in query

    field = query['field']
    field_type = getTypeOfFieldFromMapping(field, mapping)
    assert field_type in numeric_field_types
    
    boost_value = query.get('boost', 1)
    assert type(boost_value) in {float, int}

    return True
    



query_validators = {
    'bool': validateBool,
    'filter': validateFilter,
    'must': validateMust,
    'should': validateShould,
    'must_not': validateMustNot,
    'term': validateTerm,
    'terms': validateTerms,
    'match': validateMatch,
    'range': validateRange,
    'fieldBoost': validateFieldBoost,
}


# given a query and a mapping, validate that the query
# follows the rules
def validateQuery(query, mapping):
    assert type(query is dict)
    assert len(query) == 1

    op = [k for k in query][0]
    assert op in query_validators
    return query_validators[op](query[op], mapping)
