# coding=utf-8
import DNSPodX.util as util
from DNSPodX.record import Record


class Domain:
    def __init__(self, user, name):
        self.user = user
        self.name = name

    def record_list(self, offset=0, length=2000, sub_domain=None, record_type=None, record_line=None, keyword=None):
        params = {
            'domain': self.name,
            'offset': offset,
            'length': length,
            'keyword': keyword,
            'sub_domain': sub_domain,
            'record_type': record_type,
            'record_line': record_line,
        }
        params = util.remove_none(params)
        json_data = util.http_post('Record.List', self.user.login_token, params)
        record_list = []
        for item in json_data['records']:
            record_list.append(Record(self.user, self, item['name'], item['type'], item['value'],
                                      item['line'], item['ttl'], item['mx'], item['id'], item['status']))
        return record_list, json_data
