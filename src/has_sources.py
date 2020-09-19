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

    function get_connection is for making a simple connection to db and pass it later to func "get_results" to fetch datas
    function get_result uses connection and query to fetch events and returns them (count query is prefered for lower overhead)
    function get_query_aggr_field builds an aggregation query for later use in function "get_results_aggr_field"
    function get_results_aggr_field uses the aggregation query to fetch agg_values
"""

import elasticsearch
import logging
import datetime


class ElasticSearch:
    required_options = frozenset(["es_host", "es_port", "index"])

    @staticmethod
    def mute_elasticsearch():
        """
        modules "elasticsearch" and "requests" have their own loggers and sometimes their logs becomes annoying
        so here we set higher levels to avoid them
        :return:
        """
        logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

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
        start_time = tmp_args.get("start_time")
        if start_time:
            end_time = datetime.datetime.utcnow().isoformat()
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
        count_query = tmp_args.get("count_query") if tmp_args.get("count_query") else True
        if count_query:
            results = conn.count(index=index, body=query, ignore_unavailable=True)
            results = int(results["count"])
        else:
            results = conn.search(index=index, body=query, size=size, ignore_unavailable=True)
            results = int(results["hits"]["total"]["value"])
        return results

    def get_query_aggr_field(self, start_time=None, end_time=None, agg_field=None, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        filters = tmp_args.get("filters") if tmp_args.get("filters") else []
        sort = tmp_args.get("sort") if tmp_args.get("sort") else False
        desc = tmp_args.get("desc") if tmp_args.get("desc") else False
        es_filters = {'filter': {'bool': {'must': filters}}}
        start_time = tmp_args.get("start_time")
        if agg_field:
            agg_field2 = tmp_args.get("agg_field")
            if agg_field2:
                agg_field = agg_field2
        agg_size = tmp_args.get("agg_size") if tmp_args.get("agg_size") else 10
        if start_time:
            end_time = datetime.datetime.utcnow().isoformat()
        if start_time and end_time:
            es_filters['filter']['bool']['must'].insert(0, {'range': {"@timestamp": {'gt': start_time, 'lte': end_time}}})
        query = {'query': {'bool': es_filters}, "aggs": {"NAME": {"terms": {"field": agg_field, "size": agg_size}}}}
        if sort:
            query['sort'] = [{"@timestamp": {'order': 'desc' if desc else 'asc'}}]
        return query

    def get_results_aggr_field(self, conn, query, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        index = tmp_args.get("index")
        results = conn.search(index=index, body=query, size=0, ignore_unavailable=True)
        agg_field_values = []
        for result in results["aggregations"]["NAME"]["buckets"]:
            agg_field_values.append(result.get("key"))
        return agg_field_values


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

    def get_query_aggr_field(self):
        pass

    def get_results_aggr_field(self):
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

    def get_query_aggr_field(self):
        pass

    def get_results_aggr_field(self):
        pass
