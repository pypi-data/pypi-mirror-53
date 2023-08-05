import logging

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from ...client import SilkyyClient

logger = logging.getLogger(__name__)

class SilkyyDupeFilter(BaseDupeFilter):
    '''SpiderStateService request duplicates filter.

    '''
    logger = logger

    def __init__(self, project, spider, client, settings, debug=False, stats=None):
        self.project = project
        self.spider = spider
        self.client = client
        self.debug = debug
        self.settings = settings
        self.logdupes = True
        self.stats = stats

    @classmethod
    def from_settings(cls, settings):
        '''
        This method is for older scrapy version which does not support
        a spider context when building a dupefilter instance. The spider name
        will be assumed as 'spider'
        :param settings:
        :return:
        '''
        logger.debug('SilkyyDupeFilter from_settings')
        project = settings.get('BOT_NAME')
        spider = 'spider'
        client = SilkyyClient(settings.get('SILKYY_BASEURL'))
        return cls(project, spider, client, settings)

    @classmethod
    def from_crawler(cls, crawler):
        logger.debug('SilkyyDupeFilter from_crawler')
        return cls.from_spider(crawler.spider)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        project = settings.get('BOT_NAME')
        client = SilkyyClient(settings.get('SILKYY_BASEURL'))

        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(project, spider.name, client, settings, debug=debug, stats=spider.crawler.stats)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.silkyy_spider_run.seen(fp)
        return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def open(self):
        seen_expire = '7d'
        self.silkyy_spider = self.client.spider(self.project, self.spider)
        self.silkyy_spider.settings(seen_expire=seen_expire)
        self.silkyy_spider_run = self.silkyy_spider.run()

    def close(self, reason=''):
        if reason != 'finished':
            return

        error_log_count = self.stats.get_value('log_count/ERROR', 0) if self.stats else 0
        critical_log_count =  self.stats.get_value('log_count/CRITICAL', 0) if self.stats else 0
        error_count = error_log_count + critical_log_count
        commit_on_error = self.settings.getbool('SILKYY_COMMIT_ON_ERROR', False)

        logger.debug('Error count: %d' % error_count)
        logger.debug('SILKYY_COMMIT_ON_ERROR: %s' % commit_on_error)
        if commit_on_error or error_count == 0:
            logger.info('Committing silkyy spider state.')
            self.silkyy_spider_run.complete()

    def clear(self):
        pass

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)