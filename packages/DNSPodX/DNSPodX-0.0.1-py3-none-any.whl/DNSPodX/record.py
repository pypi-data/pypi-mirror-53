# coding=utf-8
import DNSPodX.util as util


class Record:
    def __init__(self, user, domain, name, r_type, value, line, ttl=None, mx=None, r_id=None, status=None):
        self.user = user
        self.domain = domain
        self.r_type = r_type
        self.status = status
        self.value = value
        self.r_id = r_id
        self.name = name
        self.line = line
        self.ttl = ttl
        self.mx = mx

    def detail(self):
        info = {
            'domain': self.domain.name,
            'record_id': self.r_id,
            'sub_domain': self.name,
            'record_type': self.r_type,
            'record_line': self.line,
            'status': self.status,
            'value': self.value,
            'ttl': self.ttl,
            'mx': self.mx,
        }
        return info

    def create(self):
        params = self.detail()
        params = util.remove_none(params)
        json_data = util.http_post('Record.Create', self.user.login_token, params)
        return self, json_data

    def modify(self):
        params = self.detail()
        params = util.remove_none(params)
        json_data = util.http_post('Record.Modify', self.user.login_token, params)
        return self, json_data

    def remove(self):
        params = {
            'domain': self.domain.name,
            'record_id': self.r_id,
        }
        params = util.remove_none(params)
        json_data = util.http_post('Record.Remove', self.user.login_token, params)
        return self, json_data

    def remark(self, remark):
        params = {
            'domain': self.domain.name,
            'record_id': self.r_id,
            'remark': remark
        }
        params = util.remove_none(params)
        json_data = util.http_post('Record.Remark', self.user.login_token, params)
        return self, json_data

    def info(self, r_id):
        self.r_id = r_id
        params = {
            'domain': self.domain.name,
            'record_id': self.r_id,
        }
        params = util.remove_none(params)
        json_data = util.http_post('Record.Info', self.user.login_token, params)
        self.mx = json_data['mx']
        self.ttl = json_data['ttl']
        self.name = json_data['name']
        self.line = json_data['line']
        self.r_type = json_data['type']
        self.value = json_data['value']
        self.status = json_data['status']
        return self, json_data
