# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class MaoyanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaoyanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None
# =============================================================================
# process_request(request, spider)
# 当每个request通过下载中间件时，该方法被调用。
# 
# process_request() 必须返回以下其中之一：一个 None 、
# 一个 Response 对象、一个 Request 对象或 raise IgnoreRequest:
# 
# 如果其返回 None ，Scrapy将继续处理该request，执行其他的中间件的相应方法，
# 直到合适的下载器处理函数(download handler)被调用， 
# 该request被执行(其response被下载)。
# 
# 如果其返回 Response 对象，Scrapy将不会调用 任何 其他的 process_request() 或 process_exception() 方法，
# 或相应地下载函数； 其将返回该response。 已安装的中间件的 process_response() 方法则会在每个response返回时被调用。
# 
# 如果其返回 Request 对象，Scrapy则停止调用 process_request方法并重新调度返回的request。
# 当新返回的request被执行后， 相应地中间件链将会根据下载的response被调用。
# 
# 如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。
# 如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。
# 如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)。
# =============================================================================

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response
# =============================================================================
# process_response(request, response, spider)
# 当下载器完成http请求，传递响应给引擎的时候调用
# 
# process_request() 必须返回以下其中之一: 返回一个 Response 对象、 
# 返回一个 Request 对象或raise一个 IgnoreRequest 异常。
# 
# 如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 
# 该response会被在链中的其他中间件的 process_response() 方法处理。
# 
# 如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。
# 处理类似于 process_request() 返回request所做的那样。
# 
# 如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 
# 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。
# =============================================================================

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
