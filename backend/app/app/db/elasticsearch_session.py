from datetime import datetime
from elasticsearch import Elasticsearch
import copy
from app.core.config import settings
from app.core.logger import Logger

from datetime import datetime

log = Logger.log(__name__)


class ElasticsearchSession:
  _es = None

  @staticmethod
  def es_client():
    if ElasticsearchSession._es is None:
      elasticsearch_uri = open("/run/secrets/elasticsearch_uri", "r").readline()
      ElasticsearchSession._es = Elasticsearch([elasticsearch_uri], http_compress=True)
    return ElasticsearchSession._es

  @staticmethod
  def celery_status(status, name=None, result_name=None):
    must = []
    if status:
      must.append({"match": {"result.status": status}})
    if name:
      must.append({"match": {"result.args": name}})
    if result_name:
      must.append({"match": {"result.name": result_name}})

    query = {
        "size": 5000,
        "query": {
            "bool": {
                "must": must
            }
        }
    }

    ElasticsearchSession.es_client().indices.refresh(index="celery")
    res = ElasticsearchSession.es_client().search(index="celery", body=query)
    log.info("Elastic Search query took :%s" % res["took"])
    if res["timed_out"]:
      log.info("Elastic Search query timeout")
    else:
      return res["hits"]["hits"]

  @staticmethod
  def search(query):
    query = {
        "query": {
            "match": {
                "address": {
                    "query": query,
                    "operator": "and",
                    "zero_terms_query": "all",
                    "fuzziness": "AUTO"
                }
            }
        }
    }

    ElasticsearchSession.es_client().indices.refresh(index="spain_address")
    res_bot = ElasticsearchSession.es_client().search(index="spain_address", body=query)
    if res_bot["timed_out"]:
      log.info("Elastic Search query timeout")
    else:
      return res_bot["hits"]["hits"]

  @staticmethod
  def index_data(address):
    # index settings
    settings = {
        "mappings": {
            "properties": {
                "address": {"type": "text", "fielddata": "true"},
                "location": {"type": "geo_point"}
            }
        }
    }

    index_name = "spain_address"

    address = copy.deepcopy(address)
    address["location"] = {'lat': address['LAT'], 'lon': address['LON']}
    address["timestamp"] = datetime.now()
    try:
      if not ElasticsearchSession.es_client().indices.exists(index_name):
        # create index
        ElasticsearchSession.es_client().indices.create(index=index_name, ignore=400, body=settings)
      ElasticsearchSession.es_client().index(index=index_name,
                                             id=address["HASH"],
                                             body=address)
    except Exception as e:
      log.error(e)
