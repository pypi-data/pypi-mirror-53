import numpy as np
# import heapq

# from .combine_scores import sum_scores

class QueryResult(object):
    def __init__(self):
        self.ids = None
        self.scores = None
    
    def getIds(self):
        return self.ids
    
    def getScores(self):
        return self.scores
    
    def getTopN(self, n, return_scores=True):
        n_clip = min(n, self.getIds().size)
        
        top_indices = np.flip(np.argpartition(self.getScores(), -n_clip)[-n_clip:])
        top_scores = np.take(self.getScores(), top_indices)
        top_scores_indices = np.flip(np.argsort(top_scores))
        top_scores_sorted = np.take(top_scores, top_scores_indices)
        top_ids_sorted = np.take(np.take(self.getIds(), top_indices), top_scores_indices)
        
        if return_scores:
            return (top_ids_sorted, top_scores_sorted)
        else:
            return (top_ids)

class EmptyQR(QueryResult):
    def __init__(self):
        self.ids = np.array([], dtype=np.int32)
        self.scores = np.array([], dtype=np.float32)

class IdsScoreQR(QueryResult):
    """
    A type of query result consisting of a numpy array of ids (integers)
    and a float16 'score' (array([1,2,4]), 1.0). 
    ex. This QR is returned by the Term query in score setting and is how postings are stored
    """
    def __init__(self):
        super().__init__()
        self.score = 1.0
    
    def getScores(self):
        if self.scores is not None:
            return self.scores
        else:
            self.scores = np.full(self.ids.size, self.score, dtype=np.float32)
            return self.scores
    
    # maybe we don't want this one
    def fromQR(self, qr):
        self.ids = qr.getIds() # might need to copy
        self.scores = qr.getScores()
        return self
    
    def fromQRScore(self, qr, score):
        self.ids = qr.getIds() # might need to copy
        self.score = score
        return self
    
    def getTopN(self, n, return_scores=True):
        top_ids = self.getIds()[0:n]
        if return_scores:
            top_scores = np.full(top_ids.size, self.score, dtype=np.float32)
            return (top_ids, top_scores)
        else:
            return (top_ids)

class IdsScoresQR(QueryResult):
    """
    A type of query result with np arrays for ids and scores
    """
    def __init__(self, ids, scores):
        self.ids = ids
        self.scores = scores
    
    def fromIdsScores(self, ids, scores):
        self.ids = ids
        self.scores = scores

class IdsQR(QueryResult):
    """
    A type of query result consisting of a numpy array of ids (integers)
    ex. This QR is returned by the Term query in filter setting
    """
    def __init__(self):
        super().__init__()
    
    def fromQR(self, qr):
        assert isinstance(qr, QueryResult)
        self.ids = qr.getIds() # might need to copy
        return self

    def fromIds(self, ids):
        assert type(ids) is np.ndarray
        self.ids = ids
        return self
    
    def getScores(self):
        if self.scores is None:
            self.scores = np.zeros(self.getIds().size, dtype=np.float32)
        return self.scores
    
    def getTopN(self, n, return_scores=True):
        top_ids = self.getIds()[0:n]
        if return_scores:
            top_scores = np.full(top_ids.size, 0, dtype=np.float32)
            return (top_ids, top_scores)
        else:
            return (top_ids)
