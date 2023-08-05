# coding=utf-8
import DNSPodX.util as util
from DNSPodX.domain import Domain


class User:
    def __init__(self, user_id, token):
        self.login_token = '{},{}'.format(user_id, token)

    def version(self):
        json_data =  util.http_post('Info.Version', self.login_token, {})
        return json_data['status']['message'], json_data

    def domain_list(self, offset=0, length=50, domain_type=None, group_id=None, keyword=None):
        params = {
            'offset': offset,
            'length': length,
            'domain_type': domain_type,
            'group_id': group_id,
            'keyword': keyword,
        }
        params = util.remove_none(params)
        json_data = util.http_post('Domain.List', self.login_token, params)
        domain_list = []
        for item in json_data['domains']:
            domain_list.append(Domain(self, item['punycode']))
        return domain_list, json_data
