import os
import base64
import json

import numpy as np
# import faiss
from google.cloud import storage
from google.cloud import bigtable
from google.cloud.bigtable import row_filters, row_set

from .query_result import IdsQR, EmptyQR, IdsScoresQR
from .analyzers import analyze
from .row_parsers import row_key_formatters, row_parsers
from .query_validator import getTypeOfFieldFromMapping


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
        schema_uri=None,
        schema=None):

        self.name = name
        self.project_id = project_id
        self.init_data_dir()

        assert schema_uri is not None or schema is not None
        if schema is not None:
            self.schema = schema
        else:
            self.schema_uri = schema_uri
            self.schema = self.load_schema()
        self.mapping = self.schema.get('mapping', {})

        self.bt_instance_id = bt_instance_id
        self.bt_table_id = bt_table_id
        
        self.bt_client = bigtable.Client(project=self.project_id)
        self.bt_instance = self.bt_client.instance(self.bt_instance_id)
        self.bt_table = self.bt_instance.table(self.bt_table_id)
        self.bt_row_filter = row_filters.CellsColumnLimitFilter(1)

        self.ttl_for_ttled_postings = int(self.schema.get('ttl', 60*5)) # 5 minutes default
        self.ttled_fields = set(self.schema.get('ttled_fields', []))
        
        self.lru_cache = LRUCache(10000)
        self.ttl_cache = TTLCache(10000, self.ttl_for_ttled_postings)
    
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


    def getPostings(self, field, value):
        field_type = getTypeOfFieldFromMapping(field, self.mapping)
        row_key = row_key_formatters[field_type](field, value)

        cached_value = None

        has_ttl = field in self.ttled_fields

        if has_ttl:
            cached_value = self.ttl_cache.get(row_key)
        else:
            cached_value = self.lru_cache.get(row_key)
        
        if cached_value is not None:
            return cached_value
        else:
            row = self.btLookup(row_key)
            fetched_qr = None
            if row is not None:
                fetched_qr = row_parsers[field_type](row)
            else:
                fetched_qr = EmptyQR()
            if has_ttl:
                self.ttl_cache[row_key] = fetched_qr
            else:
                self.lru_cache[row_key] = fetched_qr
            return fetched_qr

    def has_row_key_cached(self, row_key, field=None):
        if field is not None:
            if field in self.ttled_fields:
                return row_key in self.ttl_cache
            else:
                return row_key in self.lru_cache
        else:
            return row_key in self.lru_cache or row_key in self.ttl_cache


    def getDocument(self, i):
        row_key = 'doc|%s' % (i)
        row = self.btLookup(row_key)
        doc = None
        if row is not None:
            doc = row_parsers['doc'](row)
        return doc
    
    def getDocuments(self, doc_ids):
        row_keys = ['doc|%s' % (i) for i in doc_ids]

        documents = []

        rs = row_set.RowSet()
        set_size = 0
        for rk in row_keys:
            rs.add_row_key(rk)
            set_size += 1
        if set_size > 0:
            partial_rows_data = self.bt_table.read_rows(row_set=rs, filter_=self.bt_row_filter)
            partial_rows_data.consume_all()

            for rk in row_keys:
                row = partial_rows_data.rows.get(rk.encode())
                if row is not None:
                    doc = row_parsers['doc'](row)
                    documents.append(doc)
                else:
                    documents.append(None)
        return documents
    
    def analyze(self, field, value, return_text=True):
        spec = self.mapping
        for f in field.split('.'):
            spec = spec.get('properties', spec)
            spec = spec.get(f, {})
        analyzer_type = spec.get('analyzer', 'english')
        return analyze(value, analyzer=analyzer_type, return_text=return_text)