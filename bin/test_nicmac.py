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

configs_file = PROJECT_PATH + "/configs/memory_conf.json"

class TestNIC():

    conf = parse_json(configs_file)
    def __init__(self):
        self.conf = parse_json(configs_file)
        self.nicnum = 0

    @classmethod
    def get_number(self):
        """
        get nic number
        """
        ret = E.EFAIL
        print("1")
        cmd = "./%s/third-party/eeupdate64e |awk '/^  [0-9]/{print $1}'|wc -l"%(PROJECT_PATH)
        ret , nic_number = run_command(cmd)
        nic_number = str(nic_number).strip("\n")
        bom_nic_number = "1"#BomNicAdd()[0]             #add the function
        logger.info("The nic number : {}".format(nic_number))
        logger.info("The bom number : {}".format(bom_nic_number))
        self.nicnum = int(nic_number)
        if nic_number == bom_nic_number:
            ret = E.EOK 
        else :
            ret = E.ENICNUMB
        return ret 

    @classmethod
    def read_mac(self,argv):
        """
        Read nic miac
        """
        ret = E.EFAIL
        print(argv)
        self.get_number()
        if self.nicnum == 0:
            logger.info("Not NIC adapter found,please check")
        else :
            logger.info("The NIC number : ".format(self.nicnum))
        for num in range(self.nicnum):
            cmd = "./%s/third-party/eeupdate64e /nic=%d /MAC_DUMP |awk '/LAN MAC Address/{print substr($6, 1, length($6)-1)}'"%(PROJECT_PATH,int(num))
            ret , nicmac = run_command(cmd)
            logger.info("The NO.{} NIC mac :{}".format(num,nicmac))
        ret = E.EOK 
        return ret 

    @classmethod
    def write_mac(self,argv):
        """
        Write nic miac
        """
        ret = E.EFAIL
        print(argv)
        self.get_number()
        if self.nicnum == 0:
            logger.info("Not NIC adapter found,please check")
        else :
            logger.info("The NIC number : ".format(self.nicnum))
        sleep(2)
        cmd = "./%s/third-party/eeupdate64e /nic=%s /mac=%s"%(PROJECT_PATH,argv[1],argv[2])
        logger.info("The command : {}".format(cmd))
        ret , rc = run_command(cmd)
        sleep(3)
        if "Done" in rc :
            ret = E.EOK
            logger.info("NIC {} updating MAC to {}...Done".format(argv[1],argv[2]))
        else :
            ret = E.ENICWMAC
        return ret 

def get_nic_number():
    logger.info(common_handle(TestNIC.get_number(), test_name()))
def read_nic_mac(argv):
    logger.info(common_handle(TestNIC.read_mac(argv), test_name()))
def write_nic_mac(argv):
    logger.info(common_handle(TestNIC.write_mac(argv), test_name()))


def show_help():    
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info('     -h      --help            Display this help text and exit')
    logger.info('     -n      --number          Get nic number')
    logger.info('     -r      --read            Read nic mac')
    logger.info('     -w      --write           Write nic mac')


def nic_test_main(argv):
    """
    NIC mac main entry
    """
    get_nic_number_flag  = False
    read_nic_mac_flag   = False
    write_nic_mac_flag   = False


    try:
        opts, args = getopt.getopt(argv,"hnr:w:",["help","number","read=","write="])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            show_help()
        elif opt in ("-n", "--number"):
            get_nic_number_flag = True
        elif opt in ("-r", "--read"):
            read_nic_mac_flag  = True
        elif opt in ("-w", "--write"):
            write_nic_mac_flag  = True


    if get_nic_number_flag:
        get_nic_number()
    if read_nic_mac_flag:
        read_nic_mac(arg)
    if write_nic_mac_flag:
        write_nic_mac(arg)

if __name__ == "__main__":
    nic_test_main(sys.argv[1:])
