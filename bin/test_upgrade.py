#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import os
import sys
import time
import getopt
import threading

from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from common.common import run_command, parse_json, common_handle, test_name, logger,PROJECT_PATH
from common.errcode import E
#------------------------------------------------------------------------------

configs_file = PROJECT_PATH + "/configs/upgrade_conf.json"
fwconfigs_file = PROJECT_PATH + "/configs/firmware_conf.json"
bmc_configs_file = PROJECT_PATH + "/configs/bmc_conf.json"

class Testupgrade():

    conf = parse_json(configs_file)
    fw_path = conf['fw_path']
    def __init__(self):
        self.conf = parse_json(configs_file)
        self.fw_path = self.conf['fw_path']

    @classmethod
    def upgrade_bios(self):
        """
        upgrade bios firmware
        """
        ret = E.EFAIL
        print("1")
        return ret 

    @classmethod
    def upgrade_cpld(self):
        """
        Upgrade CPLD firmware
        """
        ret = E.EFAIL
        print("2")
        fwconfig = parse_json(self.fw_path + 'fw_update.json')["UpdateCpldFW"]
        logger.info("*****************Upgrade Start*****************")
        cmd = self.conf["upgrade_cpld_hdd"].format(self.fw_path+fwconfig['filename'])
        print(cmd)
        ret , output = run
        return ret 

    @classmethod
    def upgrade_bmc(self):
        """
        Upgrade BMC firmware
        """
        ret = E.EFAIL
        print("3")
        return ret

def RunIpmiCmd(cmd, retype='r', pre=''):
    '''IPMB Over Lan'''
    conf = parse_json(bmc_configs_file)
    host = conf["bmc_ip"]
    user = conf["lbmc_user"]
    passwd = conf["lbmc_passwd"]
    icmd = "%s ipmitool -I lanplus -H %s -U %s -P %s %s"%(pre, host, user, passwd, cmd)
    logger.info("BMC cmd:%s"%icmd)
    return Run(icmd, retype)

def upgrade_device(*args):
    args_len = len(args)
    if 2 == args_len:
        ret = RunIpmiCmd(args[0])
        if 'Error: Unable to establish IPMI v2 / RMCP+ session' in ret:
            logger.info('cmd [{}] execution failed'.format(args[0]))
            return 'open Protect Failed'
        else:
            logger.info('open Protect success')
    output = RunIpmiCmd(args[args_len - 1], pre='echo y |')
    logger.info(output)
    return output

def show_help():    
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info('     -h      --help            Display this help text and exit')
    logger.info('     -b      --bios            Upgrade BIOS firmware')
    logger.info('     -c      --cpld            Upgrade CPLD fireware')
    logger.info('     -m      --bmc             Upgrade BMC firmware')


def upgrade_test_main(argv):
    """
    Firmware upgrade main entry
    """
    upgrade_bios_flag  = False
    upgrade_cpld_flag  = False
    upgrade_bmc_flag  = False


    try:
        opts, args = getopt.getopt(argv,"hbcm",["help","bios","cpld","bmc"])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            show_help()
        elif opt in ("-b", "--bios"):
            upgrade_bios_flag = True
        elif opt in ("-c", "--cpld"):
            upgrade_cpld_flag  = True
        elif opt in ("-m", "--bmc"):
            upgrade_bmc_flag  = True


    if upgrade_bios_flag:
        logger.info(common_handle(Testupgrade.upgrade_bios(), test_name()))
    if upgrade_cpld_flag:
        logger.info(common_handle(Testupgrade.upgrade_cpld(), test_name()))
    if upgrade_bmc_flag:
        logger.info(common_handle(Testupgrade.upgrade_bmc(), test_name()))

if __name__ == "__main__":
    upgrade_test_main(sys.argv[1:])
