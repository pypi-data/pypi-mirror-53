import functools
import math
import gensim

import numpy as np

from .query_result import IdsQR, IdsScoresQR, IdsScoreQR
from mark_search.combine_scores import sorted_multi_sum_scores_must, sorted_intersect1d, sorted_multi_sum_scores, sorted_multi_union1d


class QueryComponent(object):
    """
    Abstract base class for query components such as term, match, and, or...
    Args:
        name (str): component name.
        context (:obj:`QueryContext`): Contains information about how this component
            was called. Might include limit, offset, and score/filter mode
        candidates (:obj:`QueryResult`): Results of subqueries. Might be one of many forms.
    """
    def __init__(self, name, context, candidates):
        self.name = name
        self.context = context
        self.candidates = candidates
    
    # called in the filter context
    def _filter(self):
        pass
    
    # called in the score context
    def _score(self):
        pass

# in filter setting
# returns an IdsQR containing the intersection of the candidate list qr's
# in score setting
# adds up all scores
class And(QueryComponent):
    def __init__(self, context):
        super().__init__('and', context, None)
    
    def _filter(self, candidate_list):
        candidate_list.sort(key=lambda x: x.getIds().size)
        # maybe put some logic in here to decide whether to do a linear
        # merge or a divide and conquer merge. depending on min_size:max_size:length
        return functools.reduce(lambda a, b: IdsQR().fromIds(sorted_intersect1d(a.getIds(), b.getIds(), assume_sorted=True)), candidate_list)

    def _score(self, candidate_list):
        ids_list = [e.getIds() for e in candidate_list]
        scores_list = [e.getScores() for e in candidate_list]
        ids, scores = sorted_multi_sum_scores_must(ids_list, scores_list, assume_sorted=True)
        return IdsScoresQR(ids, scores)


# in filter setting
# returns an IdsQR containing the union of the candidate list qr's
# in score setting
# adds up all scores 
class Or(QueryComponent):
    def __init__(self, context):
        super().__init__('or', context, None)

    def _filter(self, candidate_list):
        ids_list = [e.getIds() for e in candidate_list]
        return IdsQR().fromIds(sorted_multi_union1d(ids_list, assume_sorted=True))

    def _score(self, candidate_list):
        ids_list = [e.getIds() for e in candidate_list]
        scores_list = [e.getScores() for e in candidate_list]
        ids, scores = sorted_multi_sum_scores(ids_list, scores_list, assume_sorted=True)
        return IdsScoresQR(ids, scores)


class Term(QueryComponent):
    def __init__(self, context):
        super().__init__('term', context, None)
    
    def _filter(self, field, term):
        return self.context.index.getPostings(field, term)
    
    def _score(self, field, term, score=None):
        postings = self.context.index.getPostings(field, term)
        return IdsScoreQR().fromQRScore(postings, score or 1 / math.log(2 + postings.getIds().size))

class Terms(QueryComponent):
    def __init__(self, context):
        super().__init__('terms', context, None)
    
    def tokenize(self, s):
        return gensim.utils.simple_preprocess(s)
    
    def _filter(self, field, terms):
        tokens = []
        if type(terms) is str:
            tokens = self.tokenize(terms)
        elif type(terms) is list:
            tokens = terms
        term_queries = [Term(self.context)._filter(field, term) for term in tokens]
        or_query_result = Or(self.context)._filter(term_queries)
        return or_query_result
    
    def _score(self, field, terms):
        tokens = []
        if type(terms) is str:
            tokens = self.tokenize(terms)
        elif type(terms) is list:
            tokens = terms
        term_queries = [Term(self.context)._score(field, term) for term in tokens]
        print(term_queries)
        or_query_result = Or(self.context)._score(term_queries)
        return or_query_result

class Match(QueryComponent):
    def __init__(self, context):
        super().__init__('match', context, None)
    
    def _filter(self, field, terms):
        tokens = []
        if type(terms) is str:
            tokens = self.context.index.analyze(field, terms, return_text=False)
        elif type(terms) is list:
            tokens = terms
        term_queries = [Term(self.context)._filter(field, term) for term in tokens]
        or_query_result = Or(self.context)._filter(term_queries)
        return or_query_result
    
    def _score(self, field, terms):
        tokens = []
        if type(terms) is str:
            tokens = self.context.index.analyze(field, terms, return_text=False)
        elif type(terms) is list:
            tokens = terms
        term_queries = [Term(self.context)._score(field, term) for term in tokens]
        or_query_result = Or(self.context)._score([tq for tq in term_queries])
        return or_query_result

class Range(QueryComponent):
    def __init__(self, context):
        super().__init__('range', context, None)
        self.ops = {
            'gt': np.greater,
            'gte': np.greater_equal,
            'lt': np.less,
            'lte': np.less_equal
        }

    def _filter(self, field, bounds={}):
        values = self.context.index.getPostings(field, None)
        
        range_mask = None

        for bound in bounds:
            op = self.ops.get(bound)
            assert op is not None
            mask = op(values.scores, bounds[bound])
            if range_mask is None:
                range_mask = mask
            else:
                range_mask = np.logical_and(range_mask, mask)
        return IdsQR().fromIds(values.ids[range_mask])


    def _score(self, field, bounds={}):
        return IdsScoreQR().fromQRScore(self._filter(field, bounds=bounds), 1)

