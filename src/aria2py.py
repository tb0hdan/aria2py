#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
try:
    import subprocess
except ImportError:
    import subprocess32

class Aria2Command(object):
    '''
    '''
    def __init__(self, conn_uri=None):
        self.conn_uri = conn_uri if conn_uri else 'http://localhost:6800/jsonrpc'
        self.r_rpcver = '2.0'
        self.r_id = 'xxx'
        self.known_commands = ['addUri']

    def __getattr__(self, name):
        def api_call(args, **kwargs):
            jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.%s' % name,
                      'params':[['http://example.org/file']]})
            print 'API Call %s %s' % (name, kwargs)
            r = requests.post(self.conn_uri, data=jsonreq)
            return Aria2Response(r.text)

        if name in self.known_commands:
            return api_call
        else:
            raise AttributeError('Aria2Command object has no attribute %r' % name)

class Aria2Client(object):
    '''
    '''
    def __init__(self, conn_uri):
        self.aria2 = Aria2Command(conn_uri)

    def test(self):
        pass


class Aria2Response(object):
    '''
    '''
    def __init__(self, response=None):
        self.response = response if type(response) == dict else json.loads(response)

    @property
    def r_id(self):
        return self.response.get('id', None)

    @property
    def r_rpcver(self):
        return self.response.get('jsonrpc', None)

    @property
    def r_hash(self):
        return self.response.get('result', None)


if __name__ == '__main__':
    c = Aria2Client('http://localhost:6800/jsonrpc')
    response = c.aria2.addUri('z')
    print response.r_hash
