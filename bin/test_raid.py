#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_

import sys
import time
import getopt
import configparser
from os import chdir
from os.path import dirname, abspath, sep
sys.path.append(dirname(dirname(abspath(__file__))))
from common.common import run_command, parse_json, common_handle, test_name, logger,PROJECT_PATH
from common.errcode import E

binpath = dirname(abspath(__file__)) + '/'
configs_file = PROJECT_PATH + "/configs/raid_conf.json"
upgrade_path = PROJECT_PATH + "/configs/upgrade_conf.json"

class TestRaid():
    """
    this is Raid test class
    """
    raid_dev_num = 0
    conf = parse_json(configs_file)
    fw_path = parse_json(upgrade_path)['fw_path']
    conf = parse_json(configs_file)
    def __init__(self):
        self.conf = parse_json(configs_file)
        self.fw_path = parse_json(upgrade_path)['fw_path']
        self.raid_dev_num = 0


    @classmethod
    def get_raidnum(self):
        ret = E.EFAIL
        cmd = "rm -rf {}sas3ircu".format(self.fw_path)
        ret , retval  = run_command(cmd)
        cmd = "ln -s  {}/third-party/sas3ircu_linux_x64_rel/sas3ircu {}sas3ircu".format(PROJECT_PATH,self.fw_path)
        ret , retval  = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO   
        cmd = "{}sas3ircu list | grep 'Index' |wc -l".format(self.fw_path)
        ret , self.raid_dev_num = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO   
        logger.info("RAID devices num : {}".format(self.raid_dev_num))
        return E.EOK

    @classmethod
    def get_raidver(self):
        ret = E.EFAIL
        fw_error_flag=0
        bios_error_flag=0
        fw_ver_list=[]
        bios_ver_list=[]
        cmd = "rm -rf {}sas3ircu".format(self.fw_path)
        ret , retval  = run_command(cmd)
        cmd = "ln -s  {}/third-party/sas3ircu_linux_x64_rel/sas3ircu {}sas3ircu".format(PROJECT_PATH,self.fw_path)
        ret , retval  = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO 
        self.get_raidnum()
        Raid_num = int(self.raid_dev_num)
        for i in range(Raid_num):
            ret ,fw_ver = run_command("%ssas3ircu %s display |grep 'Firmware version' | awk -F ':' '{printf $2}'"%(self.fw_path,i))
            ret ,bios_ver = run_command("%ssas3ircu %s display |grep 'BIOS version' | awk -F ':' '{printf $2}'"%(self.fw_path,i))
            logger.info("The current Raid #%s firmware release version:%s Check Version: %s"%(i,self.conf['version'],fw_ver))
            logger.info("The current Raid #%s bios release version:%s Check Version: %s \n"%(i,self.conf['bios_version'],bios_ver))
            fw_ver_list.append(fw_ver)
            bios_ver_list.append(bios_ver)   
        for i in  range(Raid_num):
            if fw_ver_list[i] == self.conf['version']:
                pass
            else:
                fw_error_flag=1
            if bios_ver_list[i] == self.conf['bios_version']:
                pass
            else:
                bios_error_flag=1
        if (fw_error_flag | bios_error_flag) ==0:
            ret = E.EOK 
        else:
            ret = E.ERAIDVER
        return ret 

    @classmethod
    def update_raidfw(self):
        ret = E.EFAIL
        fw_flag=0
        uefi_bsd_rel_flag=0
        sasbios_rel_flag=0    
        cmd = "rm -rf {}sas3flash".format(self.fw_path)
        ret , retval  = run_command(cmd)
        cmd = "ln -s  {}/third-party/sas3flash_linux_x86_rel/sas3flash {}sas3flash".format(PROJECT_PATH,self.fw_path)
        ret , retval  = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO   

        cmd="%s -fwall %s"%(self.fw_path + self.conf["update_tool"],self.fw_path + self.conf["filename"])
        str="Firmware Flash Successful"
        ret , ret_str1 = run_command(cmd)
        if not str in ret_str1:
            fw_flag = 1    

        cmd="%s -b %s"%(self.fw_path + self.conf["update_tool"],self.fw_path + self.conf["uefi_bsd_rel"])
        str="Flash BIOS Image Successful"
        ret , ret_str2 = run_command(cmd)
        if not str in ret_str2:
            uefi_bsd_rel_flag = 1 

        Raid_num = int(self.raid_dev_num)
        str = "Flash BIOS Image Successful"  
        for x in range(Raid_num):
            cmd="%s -c %s -b %s"%(self.fw_path + self.conf["update_tool"],i,self.fw_path + self.conf["uefi_bsd_rel"])
            ret ,ret_strs = run_command(cmd)
            if not str in stdout:
                sasbios_rel_flag=1
        if fw_flag == 0 :
            pass
        else:
            ret = E.ERAIDFLA
        if (uefi_bsd_rel_flag | sasbios_rel_flag) ==0:
            pass
        else:
            ret = E.ERAIDBIO
        if (fw_flag | uefi_bsd_rel_flag | sasbios_rel_flag)==0:
            ret = E.EOK
        return ret

    @classmethod
    def get_raidinfo(self):
        ret = E.EFAIL
        cmd1 = "storcli64 /c0 show | awk -F ':' '{if(($1!~/Product Name/)&&($1!~/FW Version/))print $2}'"
        cmd2 = "storcli64 /c1 show | awk -F ':' '{if(($1!~/Product Name/)&&($1!~/FW Version/))print $2}'"
        ret , retval1 = run_command(cmd1)
        info1 = [x.strip() for x in retval1.split("\n")]
        logger.info("RAID 0 info : {}".format(info1))
        ret , retval2 = run_command(cmd2)
        info2 = [x.strip() for x in retval2.split("\n")]
        logger.info("RAID 1 info : {}".format(info2))
        #if
        ret = E.EOK 
        return ret 

    # @classmethod
    # def get_raidnum(self):
    #     ret = E.EFAIL
    #     raid_t=Raid_Test('storcli64')
    #     raid_t.set_jbod_off()
    #     if raid_t.create_raid5() != 0:
    #         raid_t.set_jbod_on()
    #         return 
    #     if raid_t.create_raid0() != 0:
    #         raid_t.set_jbod_on()
    #         return
    #     raid_t.set_jbod_on()   


class Raid_Test:

	def __init__(self,test_tool):
		if(os.path.exists("raid_test.log")):
			os.remove("raid_test.log")
		self.test_tool = test_tool

	def set_jbod_on(self):
		ret, result = run_command("%s /c0 set jbod=on"%self.test_tool)
		if("JBOD      ON" in result):
			logger.info("Set JBOD ON successful!")
			return 0
		else:
			logger.info("Set JBOD ON unsuccessful!")
			return 1

	def set_jbod_off(self):
		ret , result =run_command("%s /c0 set jbod=off"%self.test_tool)
		if("JBOD      OFF" in result):
			logger.info("Set JBOD OFF successful!")
			return 0
		else:
			logger.info("Set JBOD OFF unsuccessful!")
			return 1 
            
	def check(self,chkflag,data):
		return True if chkflag in data else False

	def create_raid5(self):
		errflag = 0
		eid_list = self.get_eid() 
		if len(eid_list) >= 2:
			self.clear_raid()
			cmd="%s /c0 add vd r5 drives=%s,%s,%s"%(self.test_tool,eid_list[0],eid_list[1],eid_list[2])
			ret ,result = run_command(cmd)
			logger.info(result)
			raid_info = self.raid_info_show()
			if (self.check("Add VD Succeeded",result) and self.check("RAID5",raid_info)):
				logger.info("RAID 5 check pass")
			else:
				logger.info("RAID 5 check fail")
				errflag += 1
			self.clear_raid()
		else:
			logger.info("raid 5 need greate than 5 hdd")
			errflag += 1
		return errflag
	def create_raid0(self):
		errflag = 0
		eid_list = self.get_eid()
		if (len(eid_list) >= 2):
			self.clear_raid()
			cmd="%s /c0 add vd r0 drives=%s,%s"%(self.test_tool,eid_list[0],eid_list[1])
			ret ,result = run_command(cmd)
			logger.info(result)
			raid_info = self.raid_info_show()
			if (self.check("Add VD Succeeded",result) and self.check("RAID0",raid_info)):
				logger.info("RAID 0 check pass")
			else:
				logger.info("RAID 0 check fail")
				errflag += 1
			self.clear_raid()
		else:
			logger.info("raid 0 need greate than 5 hdd")
			errflag += 1
		return errflag			
				

	def raid_info_show(self):
		cmd="%s /c0 show"%(self.test_tool)
		ret ,result = run_command(cmd)
		logger.info(result)
		return result

	def clear_raid(self):
		cmd="%s /c0/v0 delete"%self.test_tool
		ret ,result = SendCmd(cmd)
		logger.info(str(result))
		if ("Some of the specified VDs does not exist" in result['stdout']):
			logger.info("Clear raid successful")
		elif("Delete VD succeeded" in result['stdout'] ):
			logger.info("Clear raid successful")
		else:
			logger.info("Clear raid unsuccessful")
			exit(1)


	def get_eid(self):
		cmd="%s /c0 show | awk  '/HDD/{print $1}' | uniq "%self.test_tool
		eid_str=run_command(cmd)
		eid_list = [ eid for eid in eid_str.split('\n') if eid ]
		return eid_list

def count_raid_device():
    logger.info(common_handle(TestRaid.get_raidnum(), test_name()))

def check_raid_fwversion():
    logger.info(common_handle(TestRaid.get_raidver(), test_name()))

def update_raid_fw():
    logger.info(common_handle(TestRaid.update_raidfw(), test_name()))

def get_raid_info():
    logger.info(common_handle(TestRaid.get_raidinfo(), test_name()))

def test_raid_func():
    logger.info(common_handle(TestRaid.test_raidfunc(), test_name()))

def show_help():
    """
    help doc
    """
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info('     -h      --help            Display this help text')
    logger.info('     -c      --count           Count RAID devices')
    logger.info('     -v      --version         Check RAID firmware version')
    logger.info('     -u      --update          Update RAID devices')
    logger.info('     -i      --info            Get RAID infomation')
    logger.info('     -t      --test            Test RAID function')

def raid_test_main(argv):
    """
    RAID main entry
    """
    count_device_flag = False
    check_fwversion_flag = False
    update_fw_flag = False
    get_info_flag = False
    raid_test_flag = False

    try:
        opts, args = getopt.getopt(argv,"cvuit",["count","version","update","info","test"])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            show_help()
        elif opt in ("-c", "--count"):
            count_device_flag = True
        elif opt in ("-v", "--version"):
            check_fwversion_flag  = True
        elif opt in ("-u", "--update"):
            update_fw_flag  = True
        elif opt in ("-i", "--info"):
            get_info_flag  = True
        elif opt in ("-t", "--test"):
            raid_test_flag  = True        
        else :
            show_help()
        
    if count_device_flag:
        count_raid_device()
        
    if check_fwversion_flag:
        check_raid_fwversion()

    if update_fw_flag:
        update_raid_fw()

    if get_info_flag:
        get_raid_info()

    if raid_test_flag:
        test_raid_func()

if __name__ == "__main__":
    raid_test_main(sys.argv[1:])

