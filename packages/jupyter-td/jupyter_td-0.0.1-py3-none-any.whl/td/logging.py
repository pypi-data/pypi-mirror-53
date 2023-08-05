import logging
from td.log.ESHandler import ESHandler
from td.contents.util.config import conf

es_url = conf.elasticsearch_url
es_port = conf.elasticsearch_port
es_index_name = conf.elasticsearch_index_name

formatter = logging.Formatter(
    '%(asctime)s %(filename)s func:%(funcName)s[line:%(lineno)d] %(levelname)s %(message)s')

es_handle = ESHandler(hosts=[{'host': es_url, 'port': es_port}],
                      auth_type=ESHandler.AuthType.NO_AUTH,
                      es_index_name=es_index_name)
es_handle.setFormatter(formatter)

logging.getLogger().setLevel(logging.WARNING)
logging.getLogger().addHandler(es_handle)
logging.getLogger().addHandler(logging.StreamHandler())

