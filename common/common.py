#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import os
import sys
import time
import json
import uuid
# import yaml
import serial
import signal
import logging
import inspect
# import pexpect
# import requests
import subprocess

from os.path import dirname, abspath
sys.path.append((dirname(abspath(__file__))))
from common.errcode import errorcode, E

#---------Config File Path-----------------------------------------------------
PROJECT_PATH        = dirname(dirname(abspath(__file__)))
LOG_PATH            = "{}/log/".format(PROJECT_PATH)
CONFIGJSON_PATH     = "{}/configs/global_conf.json".format(PROJECT_PATH)
CONFIGYAML_PATH     = "{}/configs/global_conf.yaml".format(PROJECT_PATH)
ERRCONF_PATH        = "{}/config/error_code.json".format(PROJECT_PATH)
PLATFORM_PATH       = "{}/configs/platform_data.json".format(PROJECT_PATH)

#---------Logging config-------------------------------------------------------
log_path        = LOG_PATH + "diag.log"
class Logger():
    def __init__(self, log_level=logging.INFO, path=log_path, set_file=True):
        self.obj = logging.getLogger("EGS_Diag_tool")
        self.obj.setLevel(log_level)
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[li"
                                "ne:%(lineno)d] - %(levelname)s: %(message)s")
        if set_file:
            self.fh = logging.FileHandler(path, mode="a+")
            self.fh.setLevel(log_level)
            self.fh.setFormatter(self.formatter)
            self.obj.addHandler(self.fh)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(log_level)
        self.ch.setFormatter(self.formatter)
        self.obj.addHandler(self.ch)

    def call(self):
        return self.obj

obj = Logger()
logger = obj.call()

#----------------------------Config Operate------------------------------
def parse_json(filename=CONFIGJSON_PATH):
    with open(filename, "r") as f:
        jdata = json.load(f)
    return jdata

def write_json(jsonobj, filename=CONFIGJSON_PATH):
    with open(filename, "w") as f:
        json.dump(jsonobj, f, indent=4)

# def parse_yaml(filename=CONFIGYAML_PATH):
#     with open(filename, "r") as com_fd:
#         common_data = com_fd.read()
#         ydata = yaml.load(common_data,Loader=yaml.FullLoader)
#         return ydata

# def write_yaml(yaml_data, filename=CONFIGYAML_PATH):
#     with open(filename, "w") as com_fd:
#         yaml.dump(yaml_data, com_fd)

#----------------------------Exec command--------------------------------------
def run_command(cmd):
    logger.debug('execute_local_cmd cmd[{}]'.format(cmd))
    try:
        proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        out, err = proc.communicate()
    except Exception as err:
        proc.kill()
        raise RuntimeError(str(err))
    logger.debug('Successfully execute_local_cmd cmd: [{}]'.format(out))
    if err and proc.returncode != 0:
        return proc.returncode, err
    return 0, out.decode().strip()

def execute_cmd(cmdlist):
    ret = 0
    for cmd in cmdlist:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=sys.stderr,
            close_fds=True,
            stdout=sys.stdout,
            universal_newlines=True,
            shell=True,
            bufsize=1
        )
        proc.communicate()
        ret += proc.returncode
        signal.signal(signal.SIGINT, quit)
    return ret

#----------------------------Common function-----------------------------------
def test_name():
    return inspect.stack()[1][3]

def create_uuid():
    uuid_origin = str(uuid.uuid1())
    uuid_code = uuid_origin[:24]
    return uuid_code

def common_handle(msg, func):
    if None == msg:
        return ""
    fail_reason = errorcode.get(msg, [0x00000E00,        "Unknown error"])
    return func + " - " + fail_reason[1]

def isip_format(ip_str):
    if "." not in ip_str:
        return False
    ip_split_list = ip_str.strip().split(".")
    if len(ip_split_list) != 4:
        return False
    for i in range(4):
        try:
            ip_split_list[i] = int(ip_split_list[i])
        except:
            logger.warning("IP invalid for not number: "+ ip_str)
            return False
        if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:
            pass
        else:
            logger.warning("IP invalid: " + ip_str)
            return False
    if int(ip_split_list[0] == 0):
        logger.warning("ip format wrong")
        return False
    return True

# class remote():
#     def __init__(self, username, ip, password):
#         self.username = username
#         self.ip = ip
#         self.password = password

#     def connect(self):
#         try:
#             command = 'ssh {}@{}'.format(self.username, self.ip)
#             self.obj = pexpect.spawn(command, timeout=10)
#             expect_list = [
#                 'Host key verification failed.',
#                 'yes/no',
#                 'password:',
#                 '~',
#                 '#',
#                 'Permission denied',
#                 pexpect.TIMEOUT,
#                 pexpect.EOF
#             ]
#             while True:
#                 index = self.obj.expect(expect_list, timeout=10)
#                 if index == 0:
#                     self.obj.close()
#                     stu, content = run_command('ssh-keygen -f "/root/.ssh/known_hosts" -R {}'.format(self.ip))
#                     if "updated" not in content:
#                         ret = E.ESSH38005
#                         return ret
#                     self.obj = pexpect.spawn(command, timeout=10)
#                     continue
#                 if index == 1:
#                     self.obj.sendline("yes")
#                     continue
#                 if index == 2:
#                     self.obj.sendline(self.password)
#                     continue
#                 if index == 3 or index == 4:
#                     ret = E.EOK
#                     return ret
#                 if index == 5:
#                     self.obj.close()
#                     ret = E.ESSH38001
#                     return ret
#                 if index == 6:
#                     self.obj.close()
#                     ret = E.ESSH38002
#                     return ret
#                 if index == 7:
#                     self.obj.close()
#                     ret = E.ESSH38003
#                     return ret 
#         except BaseException as error:
#             ret = E.ESSH35004
#             return ret

#     def command(self, cmd, time=20, expect_list=['#','~']):
#         self.obj.sendline(cmd)
#         self.obj.expect('\r\n', timeout=time)
#         self.obj.expect(expect_list, timeout=time)
#         try:
#             output = self.obj.before
#             if isinstance(output,bytes):
#                 output = output.decode()
#             index = output.rfind('\r\n')
#             if index == -1:
#                 output = ''
#             else:
#                 output = output[0:index]
#                 if len(output) >0 and output[0] == '|':
#                     index = output.find('\r\n')
#                     if index == -1:
#                         output = ''
#                     else:
#                         output = output[index + 2:]
#             return output
#         except BaseException as error:
#             logger.error(error)
#             logger.error('[ remote ] Error !!! ')

#     def disconnect(self):
#         self.obj.close()


# if __name__ == "__main__":
#     run_command("ps1")
