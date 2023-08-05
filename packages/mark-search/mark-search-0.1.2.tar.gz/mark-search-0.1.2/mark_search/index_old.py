import os
import base64
import json

import numpy as np
import faiss
from google.cloud import storage
from google.cloud import bigtable
from google.cloud.bigtable import row_filters

from .query_result import IdsQR

def download_gcs_dir(project_id=None, bucket_name=None, prefix=None, dl_dir=None):
    storage_client = storage.Client(project_id)
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        filename = blob.name.replace(prefix, '') 
        print('downloading %s' % (filename))
        blob.download_to_filename(dl_dir + filename)

def parseMetadata(md):
    try:
        return json.loads(md.decode("utf-8"))
    except:
        return md.decode("utf-8")

stopwords_sets = {
    'english': {"it", "its", "itself", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "of", "at", "by", "for", "with", "to", "from", "in", "then", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}
}



class Index(object):
    """
    The data. Contains inverted index postings, faiss indices.
    """
    def __init__(self, name, 
        project_id='',
        bt_instance_id='',
        bt_table_id='',
        stopwords='english', 
        stopword_threshold=None):
        self.name = name
        self.project_id = project_id
        self.bt_instance_id = bt_instance_id
        self.bt_table_id = bt_table_id
        self.stopword_threshold = stopword_threshold
        self.stopwords = stopwords_sets[stopwords] if type(stopwords) is str else stopwords
        
        self.bt_client = bigtable.Client(project=self.project_id)
        self.bt_instance = self.bt_client.instance(self.bt_instance_id)
        self.bt_table = self.bt_instance.table(self.bt_table_id)
        self.bt_row_filter = row_filters.CellsColumnLimitFilter(1)

        self.index_dir = 'data/%s' % (self.name)
        self.ii = {}
        self.postings_dir = 'data/%s/postings/' % (self.name)
        self.faiss_index = None
    
    def downloadPostings(self, postings_uri):
        
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
        
        
        if not os.path.exists(self.postings_dir):
            postings_uri_prefix = postings_uri.replace('gs://', '')
            bucket_name = postings_uri_prefix.split('/')[0]
            path = '/'.join(postings_uri_prefix.split('/')[1:])
            # download postings files
            os.mkdir(self.postings_dir)
            download_gcs_dir(
                project_id=self.project_id,
                bucket_name=bucket_name,
                prefix=path,
                dl_dir=self.postings_dir
            )
    
    def loadPostingsFromFile(self):
        
        for fn in os.listdir(self.postings_dir):
            with open(os.path.join(self.postings_dir, fn), 'r') as f:
                for line in f:
                    p = line.split('|||')
                    row_key = p[0]
                    if len(p) > 1:
                        a = None
                        if row_key.startswith('score.'):
                            # let's have some logic in here to figure out which QR is best
                            # some scores might be sparse (searchwise_scores) for instance
                            # while some may have a non-zero value for every product
                            # TODO: revisit
                            a = np.frombuffer(base64.b64decode(p[1]), dtype=np.float16)
                        else:
                            # if we maintain a sorted postings list, we can optimize filtering greatly
                            # (n^2 ->  n)
                            a = np.sort(np.frombuffer(base64.b64decode(p[1]), dtype=np.int32))
                        if len(row_key.split('.')) < 2:
                            print('row_key not correct format: %s' % (row_key))
                        else:
                            field = row_key.split('.')[0]
                            value = '.'.join(row_key.split('.')[1:])
                            if value not in self.stopwords:
                                self.putPostings(field, value, a)
                    else:
                        print(line)
    
    def load(self, faiss_filename, postings_uri):
        self.ii = {}
        self.downloadPostings(postings_uri)
        self.loadPostingsFromFile()
    
    def btLookup(self, row_key):
        row = self.bt_table.read_row(row_key.encode('utf-8'), self.bt_row_filter)
        column_family_id = 'p'
        column_id = 'p'.encode('utf-8')
        if row is not None:
            value = row.cells[column_family_id][column_id][0].value
            return value
        else:
            return None
    
    def getProductId(self, i):
        row_key = 'i.%s' % (i)
        response = self.btLookup(row_key).decode("utf-8")
        return response

    def getMetadata(self, i):
        row_key = 'p.%s' % (i)
        response = parseMetadata(self.btLookup(row_key))
        return response

    def getRemotePostings(self, field, value):
        row_key = '%s.%s' % (field, base64.b64encode(value.encode()).decode())
        value = self.btLookup(row_key)
        if value is not None:
            return IdsQR().fromIds(np.array(np.frombuffer(value, dtype=np.int32)))
        else:
            return IdsQR().fromIds(np.array([], dtype=np.int32))

    def getPostings(self, field, value):
        key = '%s.%s' % (field, base64.b64encode(value.encode()).decode())
        if key in self.ii:
            return self.ii[key]
        else:
            return self.getRemotePostings(field, value)
    
    def putPostings(self, field, value, ids):
        key = '%s.%s' % (field, value)
        self.ii[key] = IdsQR().fromIds(ids)
