import pyodbc
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import logging

logger = logging.getLogger('event.tasks')


class Database:

    def __init__(self, database):
        logger.info("Initiating database connection to {}".format(database))
        self.connection = None
        try:
            kwargs = settings.DATABASES[database]
            driver = kwargs.get('DRIVER', None)
            server = kwargs.get('HOST', None)
            database = kwargs.get('NAME', None)
            username = kwargs.get('USER', None)
            password = kwargs.get('PASSWORD')
            using = 'DRIVER=' + driver + ';SERVER='+server+';UID='+username+';PWD=' + password + ';TrustServerCertificate=yes;Connection Timeout=120'
            self._db_connection = pyodbc.connect(using)
            self._db_cur = self._db_connection.cursor()
        except KeyError:
            raise ImproperlyConfigured("Invalid configuration {}".format(database))

    def __del__(self):
        logger.info("Closing database connection")
        self._db_connection.close()


    def query(self, query):
        logger.debug('Executing {}'.format(query))
        try:
            result = self._db_cur.execute(query)
        except Exception as error:
            logger.error('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result