#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from random import seed as rs, choice as rc
import requests
from string import ascii_lowercase as sl, digits as sg
import time
import thread
try:
    import subprocess
except ImportError:
    import subprocess32

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

class Aria2Command(object):
    '''
    '''
    def __init__(self, conn_uri=None):
        self.conn_uri = conn_uri if conn_uri else 'http://localhost:6800/jsonrpc'
        self.r_rpcver = '2.0'
        self.r_id = ''.join([rc([x for x in sl + sg]) for x in xrange(1,8)])
        self.known_commands = [
            'addUri', 'addTorrent', 'addMetalink', 'remove',
            'forceRemove', 'pause', 'pauseAll', 'forcePause',
            'forcePauseAll', 'unpause', 'unpauseAll',
            'tellStatus', 'getUris', 'getFiles',
            'getPeers', 'getServers', 'tellActive',
            'tellWaiting', 'tellStopped', 'changePosition',
            'changeUri', 'getOption', 'changeOption',
            'getGlobalOption', 'changeGlobalOption',
            'getGlobalStat', 'purgeDownloadResult',
            'removeDownloadResult', 'getVersion',
            'getSessionInfo', 'shutdown', 'forceShutdown'
        ]

    def __prepare_args__(self, name, args):
        '''
        '''
        print name, args
        return [['http://example.com']]

    def __getattr__(self, name):
        def api_call(defarg=None, **kwargs):
            kwargs['defarg'] = defarg
            params = self.__prepare_args__(name, kwargs)
            jsonreq = json.dumps({'jsonrpc': '2.0', 'id': self.r_id,
                      'method': 'aria2.%s' % name,
                      'params': params})
            print 'API Call %s %s %s' % (name, defarg, kwargs)
            r = requests.post(self.conn_uri, data=jsonreq)
            return Aria2Response(r.text)

        if name in self.known_commands:
            return api_call
        else:
            raise AttributeError('Aria2Command object has no attribute %r' % name)

class Aria2Client(object):
    '''
    '''
    def __init__(self, conn_uri=None, start_daemon=True):
        self.stopLock = False
        self.aria2 = Aria2Command(conn_uri=conn_uri)
        if start_daemon:
            self.start_daemon()

    def ariaStop(self):
        if not self.stopLock:
            self.aria2.forceShutdown()
            self.stopLock = True

    def __del__(self):
        self.ariaStop()

    def aria_daemon(self):
        '''
        '''
        proc = subprocess.Popen(['aria2c', '--enable-rpc' ,'--rpc-allow-origin-all=true'],
                        stdout=subprocess.PIPE,
                        )
        stdout_value = proc.communicate()[0]

    def start_daemon(self):
        '''
        '''
        thread.start_new_thread(self.aria_daemon,())

    def stop_daemon(self):
        self.ariaStop()

if __name__ == '__main__':
    c = Aria2Client()
    response = c.aria2.addUri('1', a='c')
    print response.r_hash


