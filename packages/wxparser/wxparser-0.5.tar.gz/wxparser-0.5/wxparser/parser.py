import logging

logger = logging.getLogger()


class WXParser(object):
    def __init__(self, response, options):
        self._response = response

    def parse(self):
        logger.info('parser test parse ')
        return {
            'title': self.parse_title(),
            'content': self.parse_content(),
            'wx_name': self.parse_wx_name(),
            'biz': self.parse_biz(),
            'read_count': self.parse_read_count(),
        }

    def parse_title(self):
        pass

    def parse_content(self):
        pass

    def parse_wx_name(self):
        pass

    def parse_biz(self):
        pass

    def parse_read_count(self):
        pass