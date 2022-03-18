#!/usr/bin/env python3
# _*_ coding:UTF-8 _*_
aaaa
import sys
import time
import getopt
import configparser
from os import chdir
from os.path import dirname, abspath, sep
sys.path.append(dirname(dirname(abspath(__file__))))
from common.common import run_command, parse_json, common_handle, test_name, \
    logger,write_json, PROJECT_PATH,  CONFIGJSON_PATH
from common.errcode import E

binpath = dirname(abspath(__file__)) + '/'
configs_file = PROJECT_PATH + "/configs/fru_conf.json"
rconfigs_file = PROJECT_PATH + "/configs/fru_riser_conf.json"
dconfigs_file = PROJECT_PATH + "/configs/dmi_conf.json"
bconfigs_file = PROJECT_PATH + "/configs/bmc_conf.json"
tool_path = PROJECT_PATH + "/third-party/"
bin_path = PROJECT_PATH + "/firmware/"
confname = "fru.conf"


class TestFRU():
    """
    this is FRU test class
    """
    conf = parse_json(configs_file)
    rconf = parse_json(rconfigs_file)
    dconf = parse_json(dconfigs_file)
    bconf = parse_json(bconfigs_file)
    def __init__(self):
        self.conf = parse_json(configs_file)
        self.rconf = parse_json(rconfigs_file)
        self.dconf = parse_json(dconfigs_file) 
        self.bconf = parse_json(bconfigs_file) 


    @classmethod
    def system_info(self):
        """
        check system info
        """
        ret = E.EFAIL
        infos = []
        cmd = """dmidecode -t 1 |sed 's/\t//g' |grep -E '^Manufacturer:|^Product Name:|^Version:|^UUID:|SKU Number:
        |Family:'|awk -F ':' '{print $2,$3,$4,$5}'"""
        ret,fru_info = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        fru_info = list(fru_info.split("\n"))
        for x in fru_info :
            x = x.strip()
            infos.append(x)
        #logger.info("\nManufacturer:{}\nProduct Name:{}\nVersion:{}\nUUID:{}\nSKU Number:{}\nFamily:{}".format(infos[0],infos[1],
        #    infos[2],infos[3],infos[4],infos[5]))
        logger.info("Manufacturer:{}".format(infos[0]))
        logger.info("Product Name:{}".format(infos[1]))
        logger.info("Version:{}".format(infos[2]))
        logger.info("UUID::{}".format(infos[3]))
        logger.info("SKU Number:{}".format(infos[4]))
        logger.info("Family:{}".format(infos[5]))
        if infos[0] == self.dconf["dmi_type1"]["manufacturer"]  and infos[1] == self.dconf["dmi_type1"]["product name"] \
            and infos[2] == self.dconf["dmi_type1"]["version"] and infos[3] == self.dconf["dmi_type1"]["uuid"] and \
            infos[4] == self.dconf["dmi_type1"]["sku number"] and infos[5] == self.dconf["dmi_type1"]["family"]:
            ret = E.EOK
        else :
            ret = E.EDMISYST
        return ret

    @classmethod
    def baseboard_info(self):  # compare style dictionary
        """
        check baseboard info
        """
        ret = E.EFAIL
        infos = []
        cmd = "dmidecode -t 2 |sed 's/\t//g' |grep -E '^Manufacturer:|^Product Name:|^Version:|^Serial Number:'|awk -F ':' '{print $2,$3}'"
        ret,fru_info = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO
        fru_info = list(fru_info.split("\n"))
        for x in fru_info:
            x = x.strip()
            infos.append(x)
        logger.info("Manufacturer:{}".format(infos[0]))
        logger.info("Product Name:{}".format(infos[1]))
        logger.info("Version:{}".format(infos[2]))
        logger.info("Serial Number:{}".format(infos[3]))
        if infos[0] == self.dconf["dmi_type2"]["manufacturer"]  and infos[1] == self.dconf["dmi_type2"]["product name"] \
            and infos[2] == self.dconf["dmi_type2"]["version"] and infos[3] == self.dconf["dmi_type2"]["serial number"] :       
            ret = E.EOK
        else :
            ret = E.EDMIBASE
        return ret 

    @classmethod
    def fru_infos(self,argv):
        """
        Get FRU infos
        """
        ret = E.EFAIL       
        cmd = "ipmitool fru print " + str(argv)
        ret,infos = run_command(cmd)
        logger.info("FRU 0 infos : {}".format(infos))
        cmd = cmd + " | awk -F ':' '{if(($1!~/Chassis Type/)&&($1!~/Board Mfg Date/))print $2}'"
        ret,infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO 
        fru_info = [x.strip() for x in infos.split("\n")] 
        for x in ["cia", "bia", "pia"]:
            for y in self.conf[x].keys():   
                z = self.conf[x][y]
                if fru_info.count(z) == 0:
                    logger.info("Wrong value : {}".format(z))
                    ret = E.EFRUREAD
                    return ret 
        ret = E.EOK
        return ret

    @classmethod
    def fru_fan_infos(self,argv):
        """
        Get FRU fan infos
        """
        ret = E.EFAIL       
        cmd = "ipmitool fru print " + str(argv)
        ret,infos = run_command(cmd)
        logger.info("FRU fans infos : {}".format(infos))
        cmd = cmd + " | awk -F ':' '{if(($1!~/Chassis Type/)&&($1!~/Board Mfg Date/))print $2}'"
        ret,infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO  
        fru_info = [x.strip() for x in infos.split("\n")]
        for x in ["cia", "bia", "pia"]:
            for y in self.conf[x].keys():
                z = self.conf[x][y]
                if fru_info.count(z) == 0:
                    logger.info("Wrong value : {}".format(z))
                    ret = E.EFRUREAD
                    return ret 
        ret = E.EOK
        return ret

    @classmethodasd 
    def fru_other_infos(self,argv):
        """
        Get FRU other infos
        """
        ret = E.EFAIL       
        cmd = "ipmitool fru print " + str(argv) + " "
        ret,infos = run_command(cmd)
        if 0 != ret:
            logger.warning("cmd exec fail: {}".format(cmd))
            return E.EIO 
        if "not found" in infos :
            ret = E.EEXIST
            return ret 
        fru_info = [x.strip() for x in infos.split("\n")]
        #if argv in range(11,13)
        logger.info(infos)
        ret = E.EOK
        return ret

    @classmethod
    def fru_program(self,argv):
        ret = E.EFAIL 
        logger.info("FRU 0 write start")
        UpdateFruConf(confname)
        FruConf2bin(confname)    
        cmd = {
            "Disable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x00",
            "Write Fru Config": "ipmitool fru write 0 {}FRU.bin".format(binpath),
            "Enable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x01"
        }
        err = []
        for x in cmd.keys():
            logger.info("%s."%x)
            err.append(run_command(cmd[x])[1])
        if any(err):
            ret = E.EOK	
        else:
            ret = E.EFRUPROG
        return ret 

    @classmethod
    def fan_program(self,argv):
        ret = E.EFAIL 
        logger.info("FRU fan write start")
        UpdateFruConf(confname)
        FruConf2bin(confname)    
        cmd = {
            "Disable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x00 2>&1",
            "Write Fru fan1 Config": "ipmitool fru write 3 {}FRU.bin 2>&1",
            "Write Fru fan2 Config": "ipmitool fru write 4 {}FRU.bin 2>&1",
            "Write Fru fan3 Config": "ipmitool fru write 5 {}FRU.bin 2>&1",
            "Write Fru fan4 Config": "ipmitool fru write 6 {}FRU.bin 2>&1",
            "Write Fru fan5 Config": "ipmitool fru write 7 {}FRU.bin 2>&1",
            "Write Fru fan6 Config": "ipmitool fru write 8 {}FRU.bin 2>&1",
            "Enable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x01 2>&1",
        }
        for x in cmd.keys():
            logger.info("%s."%x)
            ret,output = run_command(cmd[x])
        ret = E.EOK        
        if 'Bad header checksum' in output:
            ret = E.EFRUFANS
        elif 'Could not open' in output:
            ret = E.EEXIST
        return ret 

    @classmethod
    def riser_program(self,argv):
        ret = E.EFAIL 
        logger.info("Riser program start")
        confname = "fru_riser.conf"
        fru_riser_g(argv)
        UpdateFruConf(confname)
        FruConf2bin(confname)
        cmd = {
            "Disable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x00",
            "Write Fru Config": "ipmitool fru write {} {}FRU.bin".format(argv,binpath),
            "Enable Write FRU Protect": "ipmitool raw 0x3a 0x16 0x01"
        }
        err = []
        for x in cmd.keys():
            logger.info("%s."%x)
            err.append(run_command(cmd[x])[1])
        if any(err):
            ret = E.EOK	
        else:
            ret = E.EFRURISE
        return ret 
        
    @classmethod
    def check_bmcmac(self):  # 
        ret = E.EFAIL 
        mac_conf = self.conf["mia_mac"]
        mac_list = []
        lan_channel = self.bconf['lan channel'].split(',')  
        print(lan_channel)
        cmd1 = "ipmitool raw 0x0c 0x02 0x{} 0x05 0x00 0x00".format(lan_channel[0])
        ret , mac1 = run_command(cmd1)
        mac1 = mac1.replace(" ","")[2:]
        cmd2 = "ipmitool raw 0x0c 0x02 0x{} 0x05 0x00 0x00".format(lan_channel[1])
        ret , mac2 = run_command(cmd2)
        mac2 = mac2.replace(" ","")[2:]
        logger.info(mac1)
        logger.info(mac2)
        if mac1 == mac_conf["bmc_base_mac_address"] and mac2 == mac_conf["host_base_mac_address"]:
            ret = E.EOK
        else :
            ret = E.EFRUBMCM
        return ret 

    @classmethod
    def modify_bmcmac(self):
        ret = E.EFAIL         
        return ret 

def UpdateFruConf(confname):
    """
    FRU confurations update 
    """    
    temconf = parse_json(configs_file)
    if "fru.conf" in confname:
        fru_conf = parse_json(configs_file)
    elif "fru_riser.conf" in confname:
        fru_conf = parse_json(rconfigs_file)
    else :
        fru_conf = parse_json(configs_file)
    fru_conf_file = "%s%s"%(bin_path,confname)
    logger.info("Fru_conf_file = %s" %fru_conf_file)
    run_command("rm -f %sFRU.bin"%bin_path)
    #fru_conf = temconf[frukey]
    for x in fru_conf.keys():
        for y in fru_conf[x].keys():
            ModifyIni(x, y, fru_conf[x][y], fru_conf_file)
    timestamp = int((time.time() - 820454400)/60)
    ModifyIni("bia", "mfg_datetime", "%s"%timestamp, fru_conf_file)

def FruConf2bin(confname):
    """
    FRU confurations write to a bin file 
    """  
    cmd = "chmod +x {}/ipmi-fru-it".format(tool_path)
    run_command(cmd)
    cmd = "%sipmi-fru-it -s 2048 -c %s%s -o %sFRU.bin -a"%(tool_path,bin_path,confname,binpath)
    logger.info("bin_path = %s" %bin_path)
    logger.info("cmd = %s" %cmd)
    logger.info(run_command(cmd))

def fru_riser_g(risernum): 
    parm_num = 2
    jsonobj = parse_json(rconfigs_file)
    cmd = "ipmitool fru print " + risernum + " |sed 's/\t//g' |grep -E 'Board Serial|Board Part Number'|awk -F ':' '{print $2}'"
    # logger.info("cmd:%s" %cmd)
    ret,riser_info = run_command(cmd)
    infos = riser_info.split("\n")
    logger.info("Riser FRU Info:%s" %infos)
    element_number = len(infos)
    for i in range(int(element_number/parm_num)):
        per_dim = infos[parm_num * i:parm_num * (i + 1)]
        Rserial, Rpartnumber = per_dim
        jsonobj['bia']['serial_number'] = Rserial
        jsonobj['bia']['part_number'] = Rpartnumber
    write_json(jsonobj)

def ModifyIni(section, param, value, filename):
    conf = configparser.ConfigParser()
    conf.read(filename)
    conf.set(section,param,value)
    with open(filename,'w+') as f:
        conf.write(f)

def show_help():
    """
    help doc
    """
    logger.info('usage: {} [OPTIONS]'.format(__name__))
    logger.info('Options are:')
    logger.info('     -h      --help            Display this help text')
    logger.info('     -s      --system          Check system info')
    logger.info('     -b      --baseboard       Check baseboard info')
    logger.info('     -r      --read            Read FRU infos, followed with FRU ID')
    logger.info('     -w      --write           Write FRU infos, followed with FRU ID')
    logger.info('     -c      --check           Check BMC base MAC address')
    logger.info('     -m      --modify          Modify BMC base MAC address')

def check_system():
    logger.info(common_handle(TestFRU.system_info(), test_name()))

def check_baseboard():
    logger.info(common_handle(TestFRU.baseboard_info(), test_name()))
    
def check_infos(argv):
    ret = argv.isdigit()
    if ret == False :
        return E.EPARA
    if int(argv) == 0 :
        logger.info(common_handle(TestFRU.fru_infos(argv), test_name()))
    elif int(argv) in range(3,9):
        logger.info(common_handle(TestFRU.fru_fan_infos(argv), test_name()))
    else :
        logger.info(common_handle(TestFRU.fru_other_infos(argv), test_name()))

def program_infos(argv):
    ret = argv.isdigit()
    if ret == False :
        return E.EPARA
    if int(argv) == 0 :
        logger.info(common_handle(TestFRU.fru_program(argv), test_name()))
    # elif int(argv) in range(1,3):
    #     logger.info("FRU PSU cannot be written")
    elif int(argv) in range(3,9):
        logger.info(common_handle(TestFRU.fan_program(argv), test_name()))
    elif int(argv) in range(11,13):
        logger.info(common_handle(TestFRU.riser_program(argv), test_name()))
    else :
        logger.info("Wrong FRU ID")

def check_bmc_mac():
    logger.info(common_handle(TestFRU.check_bmcmac(), test_name()))

def modify_bmc_mac():
    logger.info(common_handle(TestFRU.modify_bmcmac(), test_name()))

def fru_test_main(argv):
    """
    FRU main entry
    """
    check_system_flag  = False
    check_baseboard_flag   = False
    read_infos_flag  = False
    write_infos_flag  = False
    check_mac_flag = False
    modify_mac_flag = False

    try:
        opts, args = getopt.getopt(argv,"hsbr:w:cm",["help","system","baseboard","read=","write=","check","modify"])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            show_help()
        elif opt in ("-s", "--system"):
            check_system_flag = True
        elif opt in ("-b", "--board"):
            check_baseboard_flag  = True
        elif opt in ("-r", "--read"):
            read_infos_flag  = True
        elif opt in ("-w", "--write"):
            write_infos_flag  = True
        elif opt in ("-c", "--check"):
            check_mac_flag  = True
        elif opt in ("-m", "--modify"):
            modify_mac_flag  = True
        else :
            show_help()
        
    if check_system_flag:
        check_system()
        
    if check_baseboard_flag:
        check_baseboard()

    if read_infos_flag:
        check_infos(arg)

    if write_infos_flag:
        program_infos(arg)

    if check_mac_flag:
        check_bmc_mac()

    if modify_mac_flag:
        modify_bmc_mac()

if __name__ == "__main__":
    fru_test_main(sys.argv[1:])
