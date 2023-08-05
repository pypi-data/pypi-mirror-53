from scrapy import signals
from scrapy.utils.conf import closest_scrapy_cfg
import jwt
import time


class AppleAuthDownloaderMiddleware(object):
    algorithm = 'ES256'

    def __init__(self, settings, apple_secure):
        self.apple_key = settings['APPLE_KEY']
        self.apple_iss = settings['APPLE_ISS']
        self.apple_expire = settings['APPLE_EXPIRE']
        self.apple_secure = apple_secure

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        apple_secure = ''
        root_path = '/'.join(closest_scrapy_cfg().split('/')[0:-1])
        bot_path = root_path + '/' + crawler.settings['BOT_NAME']
        with open(bot_path + crawler.settings['APPLE_SECURE']) as f:
            apple_secure = f.read()
        s = cls(crawler.settings, apple_secure)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        token = self.sign()
        request.headers['Authorization'] = 'Bearer %s' % token
        request.headers['Accept'] = 'application/a-gzip'

    def sign(self):
        expire_time = (time.time()) + 60 * self.apple_expire
        payload = {
            "iss": self.apple_iss,
            "exp": expire_time,
            "aud": "appstoreconnect-v1"
        }

        return jwt.encode(
            payload,
            self.apple_secure,
            algorithm=self.algorithm,
            headers={
                'alg': self.algorithm,
                'kid': self.apple_key,
                'typ': 'JWT'
            }
        ).decode('utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)