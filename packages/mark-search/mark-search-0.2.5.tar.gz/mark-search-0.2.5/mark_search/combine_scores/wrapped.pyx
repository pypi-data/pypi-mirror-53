cimport cython
import numpy as np
import heapq
cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t

cdef class IdsScores:
    cdef int[:] ids
    cdef float[:] scores
    def __init__(self, int[:] ids, float[:] scores):
        self.ids = ids
        self.scores = scores

cdef class Ids:
    cdef int[:] ids
    def __init__(self, int[:] ids):
        self.ids = ids

# @cython.boundscheck(False)
# def sum_scores(int[:] ids, float[:] scores, scores_dict={}, int top_n=-1):
#     sd = {}

#     if len(scores_dict) > 0:
#         sd = {key: scores_dict[key] for key in scores_dict}

#     cdef int s = 0
    
#     cdef int m = ids.size

#     for i in range(m):
#         sd[ids[i]] = sd.get(ids[i], 0) + scores[i]
    
#     if top_n > -1:
#         return heapq.nlargest(min(top_n, len(sd)), sd, key=lambda x: sd[x])
#     else:
#         return sd

# @cython.boundscheck(False)
# def sum_scores_must(int[:] ids, float[:] scores, scores_dict={}, int top_n=-1, min_should_match=0):
#     sd = {}
#     mmd = {} # min match dict

#     if len(scores_dict) > 0:
#         sd = {key: scores_dict[key] for key in scores_dict}

#     cdef int s = 0
    
#     cdef int m = ids.size

#     for i in range(m):
#         sd[ids[i]] = sd.get(ids[i], 0) + scores[i]
#         mmd[ids[i]] = mmd.get(ids[i], 0) + 1
    
#     if min_should_match > 0:
#         sd = { key: sd[key] for key in sd if mmd[key] >= min_should_match }
    
#     if top_n > -1:
#         return heapq.nlargest(min(top_n, len(sd)), sd, key=lambda x: sd[x])
#     else:
#         return sd


@cython.boundscheck(False)
def is_sorted(int[:] a):
    cdef int a_last = -2147483648
    cdef int al = a.size

    for ai in range(al):
        if a[ai] < a_last:
            return False
        else:
            a_last = a[ai]

    return True

@cython.boundscheck(False)
def sorted_intersect1d(int[:] a, int[:] b, assume_sorted=False):
    if not assume_sorted:
        assert is_sorted(a) and is_sorted(b)
    cdef int[:] ab = np.empty(min(a.size, b.size), dtype=np.int32)

    cdef int bi = 0

    cdef int al = a.size
    cdef int bl = b.size
    cdef int n_int = 0

    for ai in range(al):
        while a[ai] > b[bi] and bi < bl:
            bi += 1
        if bi == bl:
            break
        else:
            if a[ai] == b[bi]:
                # if they're the same, we add to the intersection
                # otherwise, b is greater, so we need to advance ai
                ab[n_int] = a[ai]
                bi += 1
                n_int += 1
    return np.array(ab[0:n_int])

@cython.boundscheck(False)
def sorted_in1d(int[:] a, int[:] b, assume_sorted=False, invert=False):
    if not assume_sorted:
        assert is_sorted(a) and is_sorted(b)
    cdef int[:] ab = np.ones(a.size, dtype=np.int32) if invert else np.zeros(a.size, dtype=np.int32)

    cdef int bi = 0

    cdef int al = a.size
    cdef int bl = b.size

    for ai in range(al):
        while a[ai] > b[bi] and bi < bl:
            bi += 1
        if bi == bl:
            break
        else:
            if a[ai] == b[bi]:
                # if they're the same, we add to the intersection
                # otherwise, b is greater, so we need to advance ai
                ab[ai] = 0 if invert else 1
                bi += 1
    return np.array(ab, dtype=np.bool)


@cython.boundscheck(False)
cdef int[:] sorted_union1d_internal(int[:] a, int[:] b, assume_sorted=False):
    if not assume_sorted:
        assert is_sorted(a) and is_sorted(b)
    cdef int[:] ab = np.empty(a.size + b.size, dtype=np.int32)

    cdef int bi = 0

    cdef int al = a.size
    cdef int bl = b.size
    cdef int n_int = 0

    for ai in range(al):
        while a[ai] > b[bi] and bi < bl:
            ab[n_int] = b[bi]
            bi += 1
            n_int += 1 
        ab[n_int] = a[ai]
        n_int += 1
        if a[ai] == b[bi]:
            bi += 1
    while bi < bl:
        ab[n_int] = b[bi]
        bi += 1
        n_int += 1
         
    return ab[0:n_int]

@cython.boundscheck(False)
def sorted_union1d(int[:] a, int[:] b, assume_sorted=False):
    return np.array(sorted_union1d_internal(a, b, assume_sorted=assume_sorted), dtype=np.int32)

@cython.boundscheck(False)
cdef int[:] sorted_multi_union1d_internal(list ids_list, assume_sorted=False):
    cdef int l = len(ids_list)
    cdef int split_i = 0
    cdef int[:] a_ids, b_ids
    if l == 1:
        return ids_list[0]
    elif l == 2:
        return sorted_union1d_internal(ids_list[0], ids_list[1], assume_sorted=assume_sorted)
    else:
        # we have more than two, so we need to divide
        split_i = l // 2
        a_ids = sorted_multi_union1d_internal(ids_list[:split_i], assume_sorted=assume_sorted)
        b_ids = sorted_multi_union1d_internal(ids_list[split_i:], assume_sorted=assume_sorted)

        return sorted_union1d_internal(a_ids, b_ids, assume_sorted=assume_sorted)

@cython.boundscheck(False)
def sorted_multi_union1d(list ids_list, assume_sorted=False):
    cdef int[:] ids = sorted_multi_union1d_internal(ids_list, assume_sorted=assume_sorted)
    return np.array(ids, dtype=np.int32)

@cython.boundscheck(False)
cdef IdsScores sorted_sum_scores_internal(int[:] a, float[:] af, int[:] b, float[:] bf, assume_sorted=False):
    if not assume_sorted:
        assert is_sorted(a) and is_sorted(b)
    cdef int[:] ab = np.empty(a.size + b.size, dtype=np.int32)
    cdef float[:] abf = np.empty(a.size + b.size, dtype=np.float32)

    cdef int bi = 0

    cdef int al = a.size
    cdef int bl = b.size
    cdef int n_int = 0

    for ai in range(al):
        while a[ai] > b[bi] and bi < bl:
            ab[n_int] = b[bi]
            abf[n_int] = bf[bi]
            bi += 1
            n_int += 1 
        ab[n_int] = a[ai]
        if a[ai] == b[bi]:
            abf[n_int] = af[ai] + bf[bi]
            bi += 1
        else:
            abf[n_int] = af[ai]
        n_int += 1
        
    while bi < bl:
        ab[n_int] = b[bi]
        abf[n_int] = bf[bi]
        bi += 1
        n_int += 1
         
    return IdsScores(ab[0:n_int], abf[0:n_int])

@cython.boundscheck(False)
def sorted_sum_scores(int[:] a, float[:] af, int[:] b, float[:] bf, assume_sorted=False):
    cdef IdsScores ids_scores = sorted_sum_scores_internal(a, af, b, bf, assume_sorted=assume_sorted)
    return (np.array(ids_scores.ids, dtype=np.int32), np.array(ids_scores.scores, dtype=np.float32))

@cython.boundscheck(False)
cdef IdsScores sorted_multi_sum_scores_internal(list ids_list, list scores_list, assume_sorted=False):
    cdef int l = len(ids_list)
    cdef int split_i = 0
    cdef IdsScores a_ids_scores, b_ids_scores
    if l == 1:
        return IdsScores(ids_list[0], scores_list[0])
    elif l == 2:
        return sorted_sum_scores_internal(ids_list[0], scores_list[0], ids_list[1], scores_list[1], assume_sorted=assume_sorted)
    else:
        # we have more than two, so we need to divide
        split_i = l // 2
        a_ids_scores = sorted_multi_sum_scores_internal(ids_list[:split_i], scores_list[:split_i], assume_sorted=assume_sorted)
        b_ids_scores = sorted_multi_sum_scores_internal(ids_list[split_i:], scores_list[split_i:], assume_sorted=assume_sorted)

        return sorted_sum_scores_internal(a_ids_scores.ids, a_ids_scores.scores, b_ids_scores.ids, b_ids_scores.scores, assume_sorted=assume_sorted)

@cython.boundscheck(False)
def sorted_multi_sum_scores(list ids_list, list scores_list, assume_sorted=False):
    cdef IdsScores ids_scores = sorted_multi_sum_scores_internal(ids_list, scores_list, assume_sorted=assume_sorted)
    return (np.array(ids_scores.ids, dtype=np.int32), np.array(ids_scores.scores, dtype=np.float32))

@cython.boundscheck(False)
cdef IdsScores sorted_sum_scores_must_internal(int[:] a, float[:] af, int[:] b, float[:] bf, assume_sorted=False):
    if not assume_sorted:
        assert is_sorted(a) and is_sorted(b)
    
    cdef int[:] ab = np.empty(min(a.size, b.size), dtype=np.int32)
    cdef float[:] abf = np.empty(min(a.size, b.size), dtype=np.float32)

    cdef int bi = 0

    cdef int al = a.size
    cdef int bl = b.size
    cdef int n_int = 0

    for ai in range(al):
        while a[ai] > b[bi] and bi < bl:
            bi += 1
        if bi == bl:
            break
        else:
            if a[ai] == b[bi]:
                # if they're the same, we add to the intersection
                # otherwise, b is greater, so we need to advance ai
                ab[n_int] = a[ai]
                abf[n_int] = af[ai] + bf[bi]
                bi += 1
                n_int += 1
    return IdsScores(ab[0:n_int], abf[0:n_int])

def sorted_sum_scores_must(int[:] a, float[:] af, int[:] b, float[:] bf, assume_sorted=False):
    cdef IdsScores ids_scores = sorted_sum_scores_must_internal(a, af, b, bf, assume_sorted=assume_sorted)
    return (np.array(ids_scores.ids), np.array(ids_scores.scores))


@cython.boundscheck(False)
cdef IdsScores sorted_multi_sum_scores_must_internal(list ids_list, list scores_list, assume_sorted=False):
    cdef int l = len(ids_list)
    cdef int split_i = 0
    cdef IdsScores a_ids_scores, b_ids_scores
    if l == 1:
        return IdsScores(ids_list[0], scores_list[0])
    elif l == 2:
        return sorted_sum_scores_must_internal(ids_list[0], scores_list[0], ids_list[1], scores_list[1], assume_sorted=assume_sorted)
    else:
        # we have more than two, so we need to divide
        split_i = l // 2
        a_ids_scores = sorted_multi_sum_scores_must_internal(ids_list[:split_i], scores_list[:split_i], assume_sorted=assume_sorted)
        b_ids_scores = sorted_multi_sum_scores_must_internal(ids_list[split_i:], scores_list[split_i:], assume_sorted=assume_sorted)

        return sorted_sum_scores_must_internal(a_ids_scores.ids, a_ids_scores.scores, b_ids_scores.ids, b_ids_scores.scores, assume_sorted=assume_sorted)

@cython.boundscheck(False)
def sorted_multi_sum_scores_must(list ids_list, list scores_list, assume_sorted=False):
    cdef IdsScores ids_scores = sorted_multi_sum_scores_must_internal(ids_list, scores_list, assume_sorted=assume_sorted)
    return (np.array(ids_scores.ids, dtype=np.int32), np.array(ids_scores.scores, dtype=np.float32))

@cython.boundscheck(False)
def combine_must_should(int[:] must_ids, float[:] must_scores, int[:] should_ids, float[:] should_scores, assume_sorted=False):
    if not assume_sorted:
        assert is_sorted(must_ids) and is_sorted(should_ids)
    
    cdef int[:] ab = np.empty(must_ids.size, dtype=np.int32)
    cdef float[:] abf = np.empty(must_ids.size, dtype=np.float32)

    cdef int bi = 0

    cdef int al = must_ids.size
    cdef int bl = should_ids.size

    for ai in range(al):
        ab[ai] = must_ids[ai]
        while must_ids[ai] > should_ids[bi] and bi < bl - 1:
            bi += 1
        if must_ids[ai] == should_ids[bi]:
            # if they're the same, we add their scores
            # otherwise, we just use the must score
            abf[ai] = must_scores[ai] + should_scores[bi]
        else:
            abf[ai] = must_scores[ai]
    return (ab, abf)


# products to the left of the split are the only ones to create keys
# @cython.boundscheck(False)
# def sum_scores_left_must():

