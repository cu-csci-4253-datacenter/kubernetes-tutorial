import os

class Config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        GET_HOSTS_FROM = os.environ.get('GET_HOSTS_FROM') or 'dns'
        REDIS_MASTER_SERVICE_HOST = os.environ.get('REDIS_MASTER_SERVICE_HOST') or 'localhost'
        REDIS_MASTER_SERVICE_PORT = os.environ.get('REDIS_MASTER_SERVICE_PORT') or 6379
        REDIS_SLAVE_SERVICE_HOST = os.environ.get('REDIS_SLAVE_SERVICE_HOST') or 'localhost'
        REDIS_SLAVE_SERVICE_PORT = os.environ.get('REDIS_SLAVE_SERVICE_PORT') or 6379
