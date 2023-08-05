import os
import base64
import json

import numpy as np
import faiss
from google.cloud import storage
from google.cloud import bigtable
from google.cloud.bigtable import row_filters

from .query_result import IdsQR, EmptyQR, IdsScoresQR
from .analyzers import analyze


from cachetools import cached, LRUCache, TTLCache

def download_gcs_file(project_id, gcs_uri, file_name):
    assert gcs_uri.startswith('gs://')
    a = gcs_uri[5:]
    storage_client = storage.Client(project_id)
    bucket_name = a.split('/')[0]
    blob_name = '/'.join(a.split('/')[1:])
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(file_name)

def download_gcs_dir(project_id=None, bucket_name=None, prefix=None, dl_dir=None):
    storage_client = storage.Client(project_id)
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        filename = blob.name.replace(prefix, '') 
        print('downloading %s' % (filename))
        blob.download_to_filename(dl_dir + filename)

class Index(object):
    """
    The data. Contains inverted index postings, faiss indices.
    """
    def __init__(self, name, 
        project_id='',
        bt_instance_id='',
        bt_table_id='',
        schema_uri=None):

        self.name = name
        self.project_id = project_id
        self.init_data_dir()
        assert schema_uri is not None
        
        self.schema_uri = schema_uri
        self.schema = self.load_schema()
        self.mapping = self.schema.get('mapping', {})

        self.bt_instance_id = bt_instance_id
        self.bt_table_id = bt_table_id
        
        self.bt_client = bigtable.Client(project=self.project_id)
        self.bt_instance = self.bt_client.instance(self.bt_instance_id)
        self.bt_table = self.bt_instance.table(self.bt_table_id)
        self.bt_row_filter = row_filters.CellsColumnLimitFilter(1)

        self.ttl_for_ttled_postings = 60*5 # 5 minutes
        self.ttled_fields = set()
        
        self.postings_getters = {
            'keyword': self.getKeywordPostings,
            'text': self.getTextPostings,
            'float': self.getFloatPostings,
            'integer': self.getIntPostings
        }
    
    def init_data_dir(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists(os.path.join('data', self.name)):
            os.mkdir(os.path.join('data', self.name))

    def load_schema(self):
        schema_filename = os.path.join('data', self.name, 'schema.json')
        download_gcs_file(self.project_id, self.schema_uri, schema_filename)
        
        schema_str = ''
        with open(schema_filename, 'r') as f:
            schema_str = ' '.join(f.readlines())
        
        schema = json.loads(schema_str)
        return schema
    
    def btLookup(self, row_key):
        row = self.bt_table.read_row(row_key.encode('utf-8'), self.bt_row_filter)
        return row


    def getKeywordPostings(self, field, value, spec=None):
        encoded_value = base64.b64encode(value.encode()).decode('utf-8')
        row_key = '%s|%s' % (field, encoded_value)
        row = self.btLookup(row_key)
        if row is not None:
            ids_bytes = row.cells.get('i').get('i'.encode())[0].value
            ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
            return IdsQR().fromIds(ids)
        else:
            return EmptyQR()

    def getTextPostings(self, field, value, spec=None):
        # only difference between text and keyword is we analyze the value first
        v = analyze(value, analyzer=spec.get('analyzer', 'english'), return_text=True)
        return self.getKeywordPostings(field, v, spec=spec)
    
    def getFloatPostings(self, field, value, spec=None):
        row_key = field
        row = self.btLookup(row_key)
        if row is not None:
            ids_bytes = row.cells.get('i').get('i'.encode())[0].value
            ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
            scores_bytes = row.cells.get('s').get('f'.encode())[0].value
            scores = np.array(np.frombuffer(scores_bytes, dtype=np.float32), dtype=np.float32)
            return IdsScoresQR(ids, scores)
        else:
            return EmptyQR()
    
    def getIntPostings(self, field, value, spec=None):
        row_key = field
        row = self.btLookup(row_key)
        if row is not None:
            ids_bytes = row.cells.get('i').get('i'.encode())[0].value
            ids = np.array(np.frombuffer(ids_bytes, dtype=np.int32), dtype=np.int32)
            scores_bytes = row.cells.get('s').get('i'.encode())[0].value
            scores = np.array(np.frombuffer(scores_bytes, dtype=np.float32), dtype=np.float32)
            return IdsScoresQR(ids, scores)
        else:
            return EmptyQR()

    @cached(cache=LRUCache(maxsize=10000))
    def getStaticPostings(self, field, value):
        field_type = None
        spec = self.mapping
        for f in field.split('.'):
            spec = spec.get('properties', spec)
            spec = spec.get(f, {})
        field_type = spec.get('type')
        assert field_type is not None and field_type in self.postings_getters # field must be in the mapping

        return self.postings_getters[field_type](field, value, spec=spec)
    
    @cached(cache=TTLCache(maxsize=1024, ttl=300))
    def getTTLPostings(self, field, value):
        field_type = None
        spec = self.mapping
        for f in field.split('.'):
            spec = spec.get('properties', spec)
            spec = spec.get(f, {})
        field_type = spec.get('type')
        assert field_type is not None and field_type in self.postings_getters # field must be in the mapping

        return self.postings_getters[field_type](field, value, spec=spec)

    def getPostings(self, field, value):
        if field in self.ttled_fields:
            return self.getTTLPostings(field, value)
        else:
            return self.getStaticPostings(field, value)

    def getDocument(self, i):
        row_key = 'doc|%s' % (i)
        row = self.btLookup(row_key)
        if row is None:
            return None
        else:
            response = row.cells.get('doc').get('doc'.encode())[0].value
            try:
                return json.loads(response)
            except:
                return response