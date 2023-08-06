import logging
import os
import subprocess
import sys
import time


def connect(instances):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.info('>> cloud_sql_proxy called')

    def check_running():
        log.info('>> cloud_sql_proxy - check_running called')
        netstat = subprocess.Popen(['netstat', '-peanut'], stdout=subprocess.PIPE)
        for line in netstat.stdout:
            txt = line.decode('utf-8')

            if '3306' in txt:
                els = txt.split()
                log.info('>> cloud_sql_proxy listening on {}'.format(els[3]))
                return True
        return False

    i = 1
    while check_running() is False:
        log.info('>> cloud_sql_proxy starting')
        cmd = ['{}/cloud_sql_proxy'.format(os.path.dirname(__file__)),
               '-instances={}=tcp:3306'.format(instances)]
        print(cmd)
        subprocess.Popen(cmd)
        time.sleep(i)
        i = i*2

    log.info('>> cloud_sql_proxy finished connecting')
