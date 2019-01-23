# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

import elasticsearch.helpers
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch


class ESHandler(object):

    def __init__(self):
        self._index = 'stree'
        self._type = 'business_info'
        host_infos = [{'host': '127.0.0.1', 'port': 9200}]
        self.es = Elasticsearch(host_infos,
                                sniff_on_start=True,
                                sniff_on_connection_fail=True,
                                sniffer_timeout=10)
        self.create_index()

    def create_index(self):
        r = self.es.indices.create(self._index, ignore=400)
        print (r)
        if r.get('acknowledged'):
            return True
        elif r.get('status') == 400:
            return True
        return False

    def delete_index(self):
        r = self.es.indices.delete(index=self._index, ignore=[400, 404])
        if r.get('acknowledged'):
            return True
        elif r.get('status') in [400, 404]:
            return True
        return False

    def index_write(self, data):
        self.es.index(index=self._index, doc_type=self._type, body=data)

    def bulk_write(self, package):
        actions = [
            {
		'_op_type': 'index',
		'_index': self._index,
		'_type': self._type,
		'_source': item
            } for item in package
	]
        elasticsearch.helpers.bulk(self.es, actions)

    def query(self, lucene):
        r_list = []
        if lucene.find(':') != -1:
            query = lucene
        else:
            query = '*' + lucene + '*'
        s = Search(using=self.es, index=self._index)\
                .params(request_timeout=10, timeout='10s')\
                .query('query_string', query=query, analyze_wildcard=True)
        s.execute()
        count = s.count()
        print (count)
        for hit in s[0: count]:
            r = hit.to_dict()
            print (r)
            r_list.append(r.get('node'))
        return list(set(r_list))
