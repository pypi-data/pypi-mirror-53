from .query_context import QueryContext
from .query_components import Range, Match, Terms, Term, And, Or
from .query_result import IdsQR, IdsScoresQR
from .combine_scores.wrapped import sorted_in1d, combine_must_should

import numpy as np
import time

def filterHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('filter')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return And(qc)._filter(clauses)

def mustNotHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('filter')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return Or(qc)._filter(clauses)

def mustHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('score')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return And(qc)._score(clauses)

def shouldHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('score')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return Or(qc)._score(clauses)


def boolHandler(value, qc):

    # _filter = query_part_handlers['filter'](value.get('filter'), qc) if value.get('filter') else None
    # _must_not = query_part_handlers['must_not'](value.get('must_not'), qc) if value.get('must_not') else None
    # _must = query_part_handlers['must'](value.get('must'), qc) if value.get('must') else None
    # _should = query_part_handlers['should'](value.get('should'), qc) if value.get('should') else None

    has_filter = value.get('filter') is not None
    has_must_not = value.get('must_not') is not None
    has_must = value.get('must') is not None
    has_should = value.get('should') is not None

    has_any_filter = has_filter or has_must_not
    has_any_score = has_must or has_should

    has_filter_and_must_not = has_filter and has_must_not
    has_must_and_should = has_must and has_should

    if has_any_filter:

        combined_filter_ids = None
        combined_filter_invert = False
        if has_filter:
            if has_must_not:
                # if it has both, we can combine them to a single ids list
                _filter = query_part_handlers['filter'](value.get('filter'), qc)
                _must_not = query_part_handlers['must_not'](value.get('must_not'), qc)

                # using sorted_in1d with invert=True returns the ids in the first arg that are not in the second
                combined_filter_ids = _filter.getIds()[sorted_in1d(_filter.getIds(), _must_not.getIds(), invert=True, assume_sorted=True)]
                combined_filter_invert = False
            else:
                _filter = query_part_handlers['filter'](value.get('filter'), qc)
                combined_filter_ids = _filter.getIds()
                combined_filter_invert = False
        else:
            combined_filter_ids = query_part_handlers['must_not'](value.get('must_not'), qc).getIds()
            combined_filter_invert = True

        if has_must_and_should:
            _should = query_part_handlers['should'](value.get('should'), qc)
            _must = query_part_handlers['must'](value.get('must'), qc)

            filtered_must_mask = sorted_in1d(_must.getIds(), combined_filter_ids, invert=combined_filter_invert)
            _filtered_must_qr = IdsScoresQR(_must.getIds()[filtered_must_mask], _must.getScores()[filtered_must_mask])
            fm_s_ids, fm_s_scores = combine_must_should(_filtered_must_qr.getIds(), _filtered_must_qr.getScores(), _should.getIds(), _should.getScores(), assume_sorted=True)
            return IdsScoresQR(fm_s_ids, fm_s_scores)
        elif has_must:
            _must = query_part_handlers['must'](value.get('must'), qc)

            filtered_must_mask = sorted_in1d(_must.getIds(), combined_filter_ids, invert=combined_filter_invert, assume_sorted=True)
            _filtered_must_qr = IdsScoresQR(_must.getIds()[filtered_must_mask], _must.getScores()[filtered_must_mask])
            return _filtered_must_qr
        elif has_should:
            _should = query_part_handlers['should'](value.get('should'), qc)

            filtered_should_mask = sorted_in1d(_should.getIds(), combined_filter_ids, invert=combined_filter_invert, assume_sorted=True)
            _filtered_should_qr = IdsScoresQR(_should.getIds()[filtered_should_mask], _should.getScores()[filtered_should_mask])
            return _filtered_should_qr
        else:
            return IdsQR().fromIds(combined_filter_ids)
          
    else:
        # there are not filter / must_not
        # if there is must and should we combine, otherwise, return the one present
        if has_must_and_should:
            # combine must and should
            _should = query_part_handlers['should'](value.get('should'), qc)
            _must = query_part_handlers['must'](value.get('must'), qc)
            fm_s_ids, fm_s_scores = combine_must_should(_must.getIds(), _must.getScores(), _should.getIds(), _should.getScores(), assume_sorted=True)
            return IdsScoresQR(fm_s_ids, fm_s_scores)
        elif has_must:
            _must = query_part_handlers['must'](value.get('must'), qc)
            return _must
        else:
            _should = query_part_handlers['should'](value.get('should'), qc)
            return _should
    

def termHandler(value, qc):
    assert type(value) is dict and len(value) == 1
    
    field = [key for key in value][0]
    o = value[field]
    term = o.get('value')
    assert term is not None
    boost = o.get('boost')
    
    if qc.setting == 'filter':
        assert boost is None
        return Term(qc)._filter(field, term)
    elif qc.setting == 'score':
        return Term(qc)._score(field, term, score=boost)
    else:
        assert False

def matchHandler(value, qc):
    assert type(value) is dict and len(value) == 1
    field = [key for key in value][0]
    terms = value[field]
    
    if qc.setting == 'filter':
        return Match(qc)._filter(field, terms)
    elif qc.setting == 'score':
        return Match(qc)._score(field, terms)
    else:
        assert False

def rangeHandler(value, qc):
    assert type(value is dict) and len(value) == 1
    field = [key for key in value][0]
    bounds = value[field]

    if qc.setting == 'filter':
        return Range(qc)._filter(field, bounds=bounds)
    elif qc.setting == 'score':
        return Range(qc)._score(field, bounds=bounds)
    else:
        assert False

def fieldBoostHandler(value, qc):
    assert type(value is dict)
    field = value.get('field')
    assert field is not None
    boost = value.get('boost', 1)

    if qc.setting == 'filter':
        assert False # this is a scoring only operation
    elif qc.setting == 'score':
        a = qc.index.getPostings(field, None)
        if boost != 1:
            a.scores = a.scores * boost
        return a
    else:
        assert False

query_part_handlers = {
    'bool': boolHandler,
    'filter': filterHandler,
    'must': mustHandler,
    'should': shouldHandler,
    'must_not': mustNotHandler,
    'term': termHandler,
    'match': matchHandler,
    'range': rangeHandler,
    'fieldBoost': fieldBoostHandler,
}

def doQuery(query,
        index=None,
        limit=10,
        offset=0,
        min_score=0,
        return_scores=True,
        return_doc_ids=True,
        return_product_ids=False,
        return_products=False):
    start_time = time.time()

    qc = QueryContext(index)
    qc.setSetting('score')
    assert len(query) == 1
    entrypoint = [key for key in query][0]
    ids, scores = query_part_handlers[entrypoint](query[entrypoint], qc).getTopN(limit + offset)

    query_done_time = time.time()

    start = min(offset, ids.size)
    end = min(offset + limit, ids.size)

    doc_ids = [int(_id) for _id in ids[start:end]]

    response = {}
    if return_doc_ids:
        response['docs'] = doc_ids
    if return_scores:
        response['scores'] = [float(score) for score in scores[start:end]]
    if return_product_ids:
        response['product_ids'] = [index.getProductId(i) for i in doc_ids]
    if return_products:
        response['products'] = [index.getMetadata(i) for i in doc_ids]
    
    response_done_time = time.time()

    response['query_took'] = query_done_time - start_time
    response['response_took'] = response_done_time - start_time

    return response