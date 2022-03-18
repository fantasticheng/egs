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
configs_file = PROJECT_PATH + "/configs/cpu_conf.json"

class TestCpu:
    """
    this is cpu test class
    """
    conf = parse_json(configs_file)
    def __init__(self):
        self.conf = parse_json(configs_file)

    @classmethod
    def cpu_num(self):
        """
        check cpu num
        """
        ret = E.EFAIL
        #cmd = "cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c|awk -F ' '  '{print $1}' "
        cmd = "grep 'physical id' /proc/cpuinfo|sort -u|wc -l"
        ret ,cpu_num = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info('Current CPU number: {}, conf : {}'.format(cpu_num, self.conf['cpu_num']))
        if int(cpu_num.strip()) == self.conf['cpu_num']:
            ret = E.EOK
        else:
            ret = E.ECPUNUM
        return ret

    @classmethod
    def cpu_mhz(self):
        """
        Get CPU MHz         
        """  
        ret = E.EFAIL
        cmd = "lscpu |awk -F ' ' '/CPU MHz/{print $3}'|sed  's/ //g'"
        ret ,cpu_mhz = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info('Current CPU MHz: {}, conf : {}'.format(cpu_mhz, self.conf['cpu_freq']))
        if float(cpu_mhz) >= float(self.conf['cpu_freq']):
            ret = E.EOK
        else:
            ret = E.ECPUMHZ
        return ret

    @classmethod
    def cpu_cores(self):
        """
        check cpu core
        """
        ret = E.EFAIL
        cmd = "lscpu |awk -F ' ' '/^CPU\(s\)/{print $2}'|sed 's/  //g'"
        ret ,cpu_cores = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info('Current CPU cores: {}, conf : {}'.format(cpu_cores, self.conf['cpu_cors']))
        if float(cpu_cores) == float(self.conf['cpu_cors']):
            ret = E.EOK
        else:
            ret = E.ECPUCORE
        return ret

    @classmethod
    def cpu_modelname(self):
        """
        check cpu core
        """
        ret = E.EFAIL
        cmd = "lscpu |awk -F ':' '/Model name/{print $2}'|sed  's/  //g'"
        ret ,cpu_name = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info('Current CPU modelname: {}, conf : {}'.format(cpu_name, self.conf['model_name']))
        if (cpu_name.strip()) == (self.conf['model_name']):
            ret = E.EOK
        else:
            ret = E.ECPUNAME
        return ret

    @classmethod
    def cpu_l2cache(self):
        """
        check cpu L2 cache 
        """
        ret = E.EFAIL
        cmd = "lscpu |awk -F ' ' '/L2 /{print $3}'|sed  's/  //g'"
        ret ,cpu_cache = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        logger.info('Current CPU L2cache: {}, conf : {}'.format(cpu_cache, self.conf['l2_cache']))
        if str(cpu_cache.strip()) == self.conf['l2_cache']:
            ret = E.EOK
        else:
            ret = E.ECPUCACH
        return ret

    @classmethod
    def cpu_tsc(self):
        """
        check cpu tsc 
        """
        ret = E.EFAIL
        return ret

    @classmethod
    def cpu_mcelog(self):
        """
        check cpu mcelog 
        """
        ret = E.EFAIL
        cpu_mce = os.path.exists("/var/log/mcelog")
        if cpu_mce : 
            pass
        else :
            return E.EEXIST
        logger.info("File /var/log/mcelog exists, now check its errors")
        cmd = "cat /var/log/mcelog|grep error"
        ret ,cpu_mce = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        if cpu_mce :
            ret = E.ECPUMCE
        else:
            ret = E.EOK
        return ret

    @classmethod
    def cpu_microcode(self):
        """
        check cpu microcode 
        """
        ret = E.EFAIL
        cmd = "cat /proc/cpuinfo | grep -i microcode | awk -F ':' '{printf $2}'"
        ret,cpu_mcode = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        for mcode in set(cpu_mcode.split()):
            logger.info('Current CPU Microcode: {}, conf : {}'.format(mcode, str(self.conf['cpu_microcode'])))
        if str(mcode.strip()) == self.conf['cpu_microcode']:
            ret = E.EOK
        else:
            ret = E.ECPUCODE
        return ret

    @classmethod
    def cpu_stress_test(self):       
        logger.info("cpu stress test")
        cpu_stress_cmd = "stress-ng --cpu 0 --cpu-method all -t {} --times".format(self.conf["mruntime"])
        run_command(cpu_stress_cmd)
        
    @classmethod
    def cpu_margin(self):
        ret = E.EFAIL
        logger.info("cpu margin test start")
        vol_cmd = "dmidecode -t processor |awk -F ':' '/Voltage/{print $2}' | sed  's/  //g' | head -1"
        used_cmd = "top -bi -n 2 -d 0.02"
        rc, out = run_command(vol_cmd)
        if 0 != rc:
            logger.warning("cmd exec fail: {}".format(vol_cmd))
            return E.EIO
        logger.info("Before test Volatge: {}".format(out.strip()))
        thread_stress = threading.Thread(target=self.cpu_stress_test)
        thread_stress.start()
        time.sleep(5)
        while True:
            time.sleep(1)
            rc, out = run_command(used_cmd) 
            if 0 != rc:
                logger.warning("cmd exec fail: {}".format(vol_cmd))
                return E.EIO 
            cpu_used = out.split('\n\n\n')[0].split('\n')[2].split()[1]
            if float(cpu_used) > 80.0:
                logger.info("current cpu used: {}".format(cpu_used))
                break
        rc, out = run_command(vol_cmd)
        if 0 != rc:
            logger.warning("cmd exec fail: {}".format(vol_cmd))
            return E.EIO 
        logger.info("After test Volatge: {}".format(out.strip()))
        if float(out.strip().split('V')[0]) > self.conf["cpu_vol_max"] or float(out.strip().split('V')[0]) < self.conf["cpu_vol_min"]:
            ret = E.ECPUMARGIN
            return ret          
        logger.info("cpu margin test end")
        ret = E.EOK
        return ret

     

def check_cpunum():
    """
    check cpu num
    """
    logger.info(common_handle(TestCpu.cpu_num(), test_name()))

def check_cpumhz():
    """
    check cpu mhz
    """
    logger.info(common_handle(TestCpu.cpu_mhz(), test_name()))

def check_cpucores():
    """
    check cpu cores
    """
    logger.info(common_handle(TestCpu.cpu_cores(), test_name()))

def check_cpumodelname():
    """
    check cpu modelname
    """
    logger.info(common_handle(TestCpu.cpu_modelname(), test_name()))

def check_cpul2cache():
    """
    check cpu L2 cache
    """
    logger.info(common_handle(TestCpu.cpu_l2cache(), test_name()))

def check_cputsc():
    """
    check cpu tsc
    """
    logger.info(common_handle(TestCpu.cpu_tsc(), test_name()))

def check_cpumcelog():
    """
    check cpu mcelog
    """
    logger.info(common_handle(TestCpu.cpu_mcelog(), test_name()))

def check_cpumicrocode():
    """
    check cpu microcode
    """
    logger.info(common_handle(TestCpu.cpu_microcode(), test_name()))

def test_cpumargin():
    """ 
    cpu margin test
    """
    logger.info(common_handle(TestCpu.cpu_margin(), test_name()))
 

def show_help():
    """
    help doc
    """
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info('     -h      --help            Display this help text')
    logger.info('     -n      --num             Check CPU number')
    logger.info('     -z      --mhz             Check CPU mhz')
    logger.info('     -c      --cores           Check CPU cores')
    logger.info('     -m      --modelname       Check CPU modelname')
    logger.info('     -l      --cache           Check CPU l2cache')
    logger.info('     -g      --mcelog          Check CPU mcelog')
    logger.info('     -d      --microcode       Check CPU microcode')
    logger.info('     -M      --Margin          Test CPU Margin')  

def cpu_test_main(argv):
    """
    cpu main entry
    """
    test_num_flag  = False
    test_mhz_flag   = False
    test_cores_flag   = False
    test_modelname_flag   = False
    test_cache_flag   = False
    test_tsc_flag   = False
    test_mcelog_flag   = False
    test_microcode_flag   = False
    test_margin_flag   = False

    try:
        opts, args = getopt.getopt(argv,"hnzcmltgdM",["help","num","mhz","cores","modelname","cache","tsc","mcelog","microcode","Margin"])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            show_help()
        elif opt in ("-n", "--num"):
            test_num_flag = True
        elif opt in ("-z", "--mhz"):
            test_mhz_flag  = True
        elif opt in ("-c", "--cores"):
            test_cores_flag  = True
        elif opt in ("-m", "--modelname"):
            test_modelname_flag  = True
        elif opt in ("-l", "--cache"):
            test_cache_flag  = True
        elif opt in ("-t", "--tsc"):
            test_tsc_flag  = True
        elif opt in ("-g", "--mcelog"):
            test_mcelog_flag  = True
        elif opt in ("-d", "--microcode"):
            test_microcode_flag  = True                        
        elif opt in ("-M", "--Margin"):
            test_margin_flag  = True
        else :
            show_help()

    if test_num_flag:
        check_cpunum()
    if test_mhz_flag:
        check_cpumhz()
    if test_cores_flag:
        check_cpucores()
    if test_modelname_flag:
        check_cpumodelname()
    if test_cache_flag:
        check_cpul2cache()
    if test_tsc_flag:
        check_cputsc()
    if test_mcelog_flag:
        check_cpumcelog()
    if test_microcode_flag:
        check_cpumicrocode()
    if test_margin_flag:
        test_cpumargin()

if __name__ == "__main__":
    cpu_test_main(sys.argv[1:])
