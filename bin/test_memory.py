#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import os
import sys
import time
import getopt

from os.path import dirname, abspath
import threading

sys.path.append(dirname(dirname(abspath(__file__))))
from common.common import run_command, parse_json, common_handle, test_name, logger, PROJECT_PATH
from common.errcode import E
#------------------------------------------------------------------------------

configs_file = PROJECT_PATH + "/configs/memory_conf.json"


class TestMemory():

    conf = parse_json(configs_file)

    def __init__(self):
        self.conf = parse_json(configs_file)

    @classmethod
    def mem_condition(self):
        """
        check memory condition
        """
        ret = E.EFAIL
        mem_presence = ""
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Size:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, presence = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        presence = presence.split("\n")
        for line in presence:
            line = line.strip()
            if line == "No Module Installed":
                mem_presence += "0"
            else:
                mem_presence += "1"
        logger.info('Memory presence condition: {}, conf : {}'.format(
            mem_presence, self.conf['mem presence']))
        if mem_presence == self.conf['mem presence']:
            ret = E.EOK
        else:
            ret = E.EMEMPRES
        return ret

    @classmethod
    def mem_size(self):
        """
        check memory size
        """
        ret = E.EFAIL
        mem_info = []
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Size:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for x in mem_infos:
            x = x.strip()  #x
            if x == "No Module Installed":
                pass
            else:
                mem_info.append(x)
        logger.info('Current Memory size: {}, conf : {}'.format(
            mem_info, self.conf['size']))
        for x in mem_info:
            if x == self.conf['size']:
                ret = E.EOK
            else:
                ret = E.EMEMSIZE
                return ret
        return ret

    @classmethod
    def mem_locator(self):
        """
        check memory locator
        """
        ret = E.EFAIL
        mem_info = []
        cmd = """dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Locator:'|
            awk -F ':' '{print $2,$3,$4,$5}'"""
        ret ,mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for single_info in mem_infos:
            single_info = single_info.strip()
            if single_info == "NO DIMM":
                pass
            else :
                mem_info.append(single_info)
        logger.info('Current Memory locator: {} \nconf : {}'.format(mem_info, \
            self.conf['locator']))
        for locator in mem_info :
            if locator in self.conf['locator']:
                ret = E.EOK
            else :
                ret = E.EMEMLOCA
                return ret 
        return ret

    @classmethod
    def mem_type(self):
        """
        check memory type
        """
        ret = E.EFAIL
        mem_info = []
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Type:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for x in mem_infos:
            x = x.strip()  #x
            if x == "Unknown":
                pass
            else:
                mem_info.append(x)
        logger.info('Current Memory type: {}, conf : {}'.format(
            mem_info, self.conf['type']))
        for x in mem_info:
            if x == self.conf['type']:
                ret = E.EOK
            else:
                ret = E.EMEMTYPE
                return ret
        return ret

    @classmethod
    def mem_speed(self):
        """
        check memory speed
        """
        ret = E.EFAIL
        mem_info = []
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Speed:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for x in mem_infos:
            x = x.strip()
            if x == "Unknown":
                pass
            else:
                mem_info.append(x)
        logger.info('Current Memory speed: {}, conf : {}'.format(
            mem_info, self.conf['speed']))
        for x in mem_info:
            if x == self.conf['speed']:
                ret = E.EOK
            else:
                ret = E.EMEMSPEE
                return ret
        return ret

    @classmethod
    def mem_manufacturer(self):
        """
        check memory manufacturer
        """
        ret = E.EFAIL
        mem_info = []
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Manufacturer:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for x in mem_infos:
            x = x.strip()
            if x == "NO DIMM":
                pass
            else:
                mem_info.append(x)
        logger.info('Current Memory manufacturer: {}, conf : {}'.format(
            mem_info, self.conf['vendor']))
        for x in mem_info:
            if x == self.conf['vendor']:
                ret = E.EOK
            else:
                ret = E.EMEMMANU
                return ret
        return ret

    @classmethod
    def mem_partnumber(self):
        """
        check memory part number
        """
        ret = E.EFAIL
        mem_info = []
        cmd = "dmidecode -t 'Memory'|sed 's/\t//g' |grep -E '^Part Number:'|awk -F ':' '{print $2,$3,$4,$5}'"
        ret, mem_infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_infos = list(mem_infos.split("\n"))
        for x in mem_infos:
            x = x.strip()
            if x == "NO DIMM":
                pass
            else:
                mem_info.append(x)
        logger.info('Current Memory part number: {}, conf : {}'.format(
            mem_info, self.conf['part number']))
        for x in mem_info:
            if x == self.conf['part number']:
                ret = E.EOK
            else:
                ret = E.EMEMPART
                return ret
        return ret

    @classmethod
    def mem_test(self):
        """
        test memory
        """
        ret = E.EFAIL
        test_percent = 0
        test_percent = self.conf['mem_test_percent']
        cmd = "free -m"
        ret, mem_free_size = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        mem_free_size = mem_free_size.split()
        mem_test_size = int(mem_free_size[9])
        test_percent = int(test_percent.strip("%"))
        mem_test_size = int(mem_test_size * test_percent * 0.01)
        #cmd = "./../third-party/memtester {} 1".format(mem_test_size)
        cmd = "./../third-party/memtester 5 1"
        ret, test_result = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info("{}".format(test_result))
        if "FAIL" in test_result:
            ret = E.EMEMTEST
        else:
            ret = E.EOK
        return ret

    @classmethod
    def mem_ecc(self):
        """
        check ECC errors
        """
        ret = E.EFAIL
        cmd = "ipmitool sel list|sed 's/\t//g'|grep -E 'error'|awk -F '|' '{if($5!=line)print $5; line=$5}'" 
        ret, error_info = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        error_info_len = len(error_info)
        if error_info_len != 0:
            for index in range(error_info_len):
                string = error_info[index]
                error_info[index] = string.strip()
            logger.info(error_info)
            if self.conf['errortype'] in error_info:
                logger.info("Memory ECC Error Occurrence")
                ret = E.EMEMECCE
            else:
                ret = E.EOK
        else:
            ret = E.EOK
        return ret

    @classmethod
    def mem_stress(self):
        logger.info("mem stress test")
        test_size_percent = self.conf["usize"]
        test_time = self.conf["mruntime"]
        mem_stress_cmd = "stress-ng --vm 1 --vm-bytes {} --vm-method all --verify -v -t {}".format(
            test_size_percent, test_time)
        run_command(mem_stress_cmd)

    @classmethod
    def mem_margin(self):
        """
        Memory Margin test
        """
        ret = E.EFAIL
        logger.info("Memory Margin Test start")
        MemoryVref = [0.0, 0.0, 0.0, 0.0]
        memory_verf_channel = ('CPU0_ABCD_DDR4', 'CPU0_EFGH_DDR4',
                               'CPU1_ABCD_DDR4', 'CPU1_EFGH_DDR4')
        mem_verf_info_cmd = "ipmitool sdr get \"{}\" |sed 's/\t//g'|grep -E 'Sensor Reading'| awk '{{print $4}}'"
        thread_stress = threading.Thread(target=self.mem_stress)
        thread_stress.start()
        time.sleep(1)
        for i in range(4):
            rc, result = run_command(
                mem_verf_info_cmd.format(memory_verf_channel[i]))
            if rc != 0 or len(result) <= 0:
                ret = E.EIO
                return ret
            logger.info("{} sdr get value : {}".format(memory_verf_channel[i],
                                                       result))
            MemoryVref[i] = float(result)
            logger.info("Under test, {} Verf : {}".format(
                memory_verf_channel[i], MemoryVref[i]))
        for i in range(4):
            if float(MemoryVref[i]) < float(self.conf["minvref"]) or float(
                    MemoryVref[i]) > float(self.conf["maxvref"]):
                ret = E.EMEMMARG
                return ret
        logger.info("Memory Margin Test end")
        ret = E.EOK
        return ret


def check_memcondition():
    logger.info(common_handle(TestMemory.mem_condition(), test_name()))


def check_memsize():
    logger.info(common_handle(TestMemory.mem_size(), test_name()))


def check_memlocator():
    logger.info(common_handle(TestMemory.mem_locator(), test_name()))


def check_memtype():
    logger.info(common_handle(TestMemory.mem_type(), test_name()))


def check_memspeed():
    logger.info(common_handle(TestMemory.mem_speed(), test_name()))


def check_memmanu():
    logger.info(common_handle(TestMemory.mem_manufacturer(), test_name()))


def check_memnum():
    logger.info(common_handle(TestMemory.mem_partnumber(), test_name()))


def test_memory():
    logger.info(common_handle(TestMemory.mem_test(), test_name()))


def test_memecc():
    logger.info(common_handle(TestMemory.mem_ecc(), test_name()))


def test_memmargin():
    logger.info(common_handle(TestMemory.mem_margin(), test_name()))


def show_help():
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info(
        '     -h      --help            Display this help text and exit')
    logger.info(
        '     -c      --condition       Display Memory install condition')
    logger.info('     -s      --size            Get Memory size')
    logger.info('     -l      --locator         Get Memory locator')
    logger.info('     -t      --type            Get Memory type')
    logger.info('     -e      --speed           Get Memory speed')
    logger.info('     -m      --manufacturer    Get Memory manufacturer')
    logger.info('     -p      --partnumber      Get Memory partnumber')
    logger.info('     -T      --Test            Test Memory DDR')
    logger.info('     -E      --ECC             Check Memory ECC error')
    logger.info('     -M      --Margin          Test Memory Margin')


def memory_test_main(argv):
    """
    memory main entry
    """
    test_condition_flag = False
    test_size_flag = False
    test_locator_flag = False
    test_type_flag = False
    test_speed_flag = False
    test_manu_flag = False
    test_partnum_flag = False
    test_memory_flag = False
    test_ecc_flag = False
    test_margin_flag = False

    try:
        opts, args = getopt.getopt(argv, "hcsltempTEM", [
            "help", "condition", "size", "locator", "type", "speed",
            "manufacturer", "partnumber", "Test", "ECC", "Margin"
        ])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
        elif opt in ("-c", "--condition"):
            test_condition_flag = True
        elif opt in ("-s", "--size"):
            test_size_flag = True
        elif opt in ("-l", "--locator"):
            test_locator_flag = True
        elif opt in ("-t", "--type"):
            test_type_flag = True
        elif opt in ("-e", "--speed"):
            test_speed_flag = True
        elif opt in ("-m", "--manufacturer"):
            test_manu_flag = True
        elif opt in ("-p", "--partnumber"):
            test_partnum_flag = True
        elif opt in ("-T", "--Test"):
            test_memory_flag = True
        elif opt in ("-E", "--ECC"):
            test_ecc_flag = True
        elif opt in ("-M", "--Margin"):
            test_margin_flag = True

    if test_condition_flag:
        check_memcondition()
    if test_size_flag:
        check_memsize()
    if test_locator_flag:
        check_memlocator()
    if test_type_flag:
        check_memtype()
    if test_speed_flag:
        check_memspeed()
    if test_manu_flag:
        check_memmanu()
    if test_partnum_flag:
        check_memnum()
    if test_memory_flag:
        test_memory()
    if test_ecc_flag:
        test_memecc()
    if test_margin_flag:
        test_memmargin()


if __name__ == "__main__":
    memory_test_main(sys.argv[1:])