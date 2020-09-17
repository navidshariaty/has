import elasticsearch


class ElasticSearch:
    def __init__(self, host, port, use_ssl=False, verfiy_certs=False, ca_certs=None, http_auth=None, timeout=10):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.verify_certs = verfiy_certs
        self.ca_certs = ca_certs
        self.http_auth = http_auth
        self.timeout = timeout

    def get_connection(self):
        return elasticsearch.Elasticsearch(host=self.host, port=self.port, use_ssl=self.use_ssl,
                                           verify_certs=self.verify_certs,
                                           ca_certs=self.ca_certs,
                                           connection_class=elasticsearch.RequestsHttpConnection,
                                           http_auth=self.http_auth, timeout=self.timeout)

    def get_query(self, filters, start_time=None, end_time=None, sort=False, desc=True):
        es_filters = {'filter': {'bool': {'must': filters}}}
        if start_time and end_time:
            es_filters['filter']['bool']['must'].insert(0, {'range': {"@timestamp": {'gt': start_time, 'lte': end_time}}})
        query = {'query': {'bool': es_filters}}
        if sort:
            query['sort'] = [{"@timestamp": {'order': 'desc' if desc else 'asc'}}]
        return query

    def get_result(self, es_conn, index, size, query, count_query=False):
        if count_query:
            results = es_conn.count(index=index, body=query, size=size, ignore_unavailable=True)
            print()
        else:
            results = es_conn.search(index=index, body=query, size=size, ignore_unavailable=True)
