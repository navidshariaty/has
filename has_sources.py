"""
this module has a class for connecting to databases of monitoring tools, perform queries and fetch results
each class should have a variable "required_options" contains all required fields for verification process
in attribute "get_query()" we have:
    :param start_time
    :param end_time
    :param args including
        :param filters
        :param sort
        :param desc
"""

import elasticsearch
import logging


class ElasticSearch:
    required_options = frozenset(["es_host", "es_port", "index"])

    @staticmethod
    def mute_elasticsearch():
        es_logger = logging.getLogger('elasticsearch')
        es_logger.setLevel(logging.WARNING)

    def __init__(self, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        self.host = tmp_args.get("es_host")
        self.port = tmp_args.get("es_port")
        self.use_ssl = tmp_args.get("use_ssl")
        self.verify_certs = tmp_args.get("verify_certs")
        self.ca_certs = tmp_args.get("ca_certs")
        self.http_auth = tmp_args.get("username")+":"+tmp_args.get("password") if tmp_args.get("username") and tmp_args.get("password") else None
        self.timeout = tmp_args.get("timeout")
        ElasticSearch.mute_elasticsearch()

    def get_connection(self):
        return elasticsearch.Elasticsearch(host=self.host, port=self.port, use_ssl=self.use_ssl,
                                           verify_certs=self.verify_certs,
                                           ca_certs=self.ca_certs,
                                           connection_class=elasticsearch.RequestsHttpConnection,
                                           http_auth=self.http_auth, timeout=self.timeout)

    def get_query(self, start_time=None, end_time=None, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        filters = tmp_args.get("filters") if tmp_args.get("filters") else []
        sort = tmp_args.get("sort") if tmp_args.get("sort") else False
        desc = tmp_args.get("desc") if tmp_args.get("desc") else False
        es_filters = {'filter': {'bool': {'must': filters}}}
        if start_time and end_time:
            es_filters['filter']['bool']['must'].insert(0, {'range': {"@timestamp": {'gt': start_time, 'lte': end_time}}})
        query = {'query': {'bool': es_filters}}
        if sort:
            query['sort'] = [{"@timestamp": {'order': 'desc' if desc else 'asc'}}]
        return query

    def get_result(self, conn, query, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        index = tmp_args.get("index")
        size = tmp_args.get("size") if tmp_args.get("size") else 10000
        count_query = tmp_args.get("count_query")
        if count_query:
            results = conn.count(index=index, body=query, size=size, ignore_unavailable=True)
        else:
            results = conn.search(index=index, body=query, size=size, ignore_unavailable=True)
        return results


class Prometheus:
    required_options = frozenset([""])

    def __init__(self):
        pass

    def get_connection(self):
        pass

    def get_query(self):
        pass

    def get_result(self):
        pass


class Zabbix:
    required_options = frozenset([""])

    def __init__(self):
        pass

    def get_connection(self):
        pass

    def get_query(self):
        pass

    def get_result(self):
        pass
