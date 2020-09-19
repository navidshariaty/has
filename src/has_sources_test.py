import unittest
import has_sources


class MyTestCase(unittest.TestCase):
    def test_elasticsearch(self):
        es_instance = has_sources.ElasticSearch({})
        es_conn = es_instance.get_connection()
        instance_elastic_query1 = has_sources.ElasticSearch.get_query(es_conn, None, None, {})
        instance_elastic_query2 = has_sources.ElasticSearch.get_query(es_conn, None, None, {"filters": [{"match": {"test": "test2"}}]})

        self.assertDictEqual(instance_elastic_query1, {"query": {"bool": {"filter": {"bool": {"must": []}}}}})
        self.assertDictEqual(instance_elastic_query2, {"query": {"bool": {"filter": {"bool": {"must": [{"match": {"test": "test2"}}]}}}}})


if __name__ == '__main__':
    unittest.main()
