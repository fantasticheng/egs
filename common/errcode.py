from enum import IntEnum, unique

@unique
class E(IntEnum):
    EOK                = 0                # Pass
    EFAIL              = 1                # Fail
    EIO                = 2                # I/O error
    EEXIST             = 3                # files not exists
    ESUPPORT           = 4                # unsupported ops

    ELOGSEL            = 1000             # sel log check fail
    ELOGSDR            = 1001             # sdr log check fail
    ELOGDMESG          = 1002             # dmesg log check fail
    ELOGMCELOG         = 1003             # mcelog log check fail
    ELOGMESSAGE        = 1004             # message log check fail 

    ECPUNUM            = 2001             # cpu num check fail
    ECPUMHZ            = 2002             # cpu mhz check fail
    ECPUCORE           = 2003             # cpu core check fail
    ECPUNAME           = 2004             # cpu name check fail
    ECPUCACH           = 2005             # cpu l2_cache check fail
    ECPUMCE            = 2006             # cpu mcelog check fail
    ECPUCODE           = 2007             # cpu microcode check fail

    EMEMPRES           = 3001             # memory presence check fail   
    EMEMSIZE           = 3002             # memory size check fail   
    EMEMLOCA           = 3003             # memory locator check fail
    EMEMTYPE           = 3004             # memory type check fail
    EMEMSPEE           = 3005             # memory speed check fail
    EMEMMANU           = 3006             # memory manufacturer check fail
    EMEMPART           = 3007             # memory part number check fail
    EMEMTEST           = 3008             # memory test fail
    EMEMECCE           = 3009             # memory ecc check fail
    EMEMMARG           = 3010             # memory margin test fail

    ESSDNAME           = 4000             # ssd name check fail
    ESSDNUM            = 4001             # ssd number check  fail
    ESSDSIZE           = 4002             # ssd size check fail
    ESSDMODEL          = 4003             # ssd model check fail
    ESSDDEVICE         = 4004             # ssd device name get fail
    ESSDHEALTH         = 4005             # ssd smart info check fail
    ESSDIOPS           = 4006             # ssd iops check fail
    ESSDSPEED          = 4007             # ssd speed check fail

    EVERSIONBMCMAIN    = 5000                # check bmc main version fail
    EVERSIONBMCBACKUP  = 5001              # check bmc backup version fail
    EVERSIONBMC        = 5002              # check bmc version fail
    EVERSIONBIOS       = 5003              # check bios version fail
    EVERSIONCPLDMAIN   = 5004              # check cpld main version fail
    EVERSIONCPLDBACKUP = 5005             # check cpld backup version fail
    EVERSIONCPLDHDD    = 5006             # check cpld HDD version fail
    EVERSIONI210       = 5007             # check I210 version fail
    EVERSIONI350       = 5008             # check I350 version fail
    EVERSIONMT2770     = 5009             # check MT2770 version fail 
    EVERSIONPSU        = 5010             # check psu version fail
    EVERSIONPSUHW      = 5011             # check psu hw version fail
    EVERSIONPSUSW      = 5012             # check psu sw version fail
    EVERSIONEXPANDER   = 5013             # check expander version fail
    EVERSIONHDD        = 5014             # check HDD version fail
    EVERSIONVR         = 5015             # check VR version fail
    EVERSIONRAID       = 5016             # check raid version fail
    EVERSIONRAIDFW     = 5017             # check raid fw version fail
    EVERSIONRAIDBIOS   = 5018             # check raid bios version fail
    EVERSIONREIGN      = 5019             # nic firmware version not in place
    EVERSIONCPLD12BP   = 5020             # check cpld 12 bp version fail
    EVERSIONCPLD4BP    = 5021             # check cpld 4 bp version fail 

    EFRUREAD           = 7001             # FRU read fail
    EDMISYST           = 7002             # Check system info fail
    EDMIBASE           = 7003             # Check baseboard info fail
    EFRUPROG           = 7004             # FRU 0 program fail
    EFRURISE           = 7005             # FRU 11~12 program fail
    EFRUFANS           = 7006             # FRU 3~8 program fail
    EFRUBMCM           = 7007             # BMC MAC address uncorrect

    EPCIECARDNUM       = 8000             # PCIE Card Num Invalid
    EPCIECARDUNMATCH   = 8001             # PCIE Card Data Unmatch

    ERTCSET            = 13000            # set rtc fail
    ERTCCHECK          = 13001            # check rtc fail

    EUARTOPEN          = 15001
    EUARTDATA          = 15002

    EVAGTEST           = 16001

    EI2CNODEV          = 17001

    ERTCBAT            = 18001

    EPSUREIGN          = 19000            # psu not in place 
    EPSUMODEL          = 19001            # check psu model fail
    EPSUTEMP           = 19002            # check psu temperature fail
    EPSUNUM            = 19003            # check psu num fail
    EPSUSTATUS         = 19004            # check psu status fail
    EPSUTEMPNC         = 19005            # psu temperature is slightly higher or low,but nothing serious
    EPSUTEMPCR         = 19006            # psu temperature is too high or very low and very serious
    EPSUTEMPNA         = 19007            # psu temperature is unknown and irrecoverable
    EPSUINSERTION      = 19008            # psu insertion is error

    EFANPRESENT        = 20001
    EFANPWM            = 20002

    ELOGCLEAR          = 27000            # clear log fail

    ESSH35004          = 35004

    ESSH38001          = 38001
    ESSH38002          = 38002
    ESSH38003          = 38003
    ESSH38004          = 38004
    ESSH38005          = 38005
    ESSH38006          = 38006

    ESCP39001          = 39001
    ESCP39002          = 39002
    ESCP39003          = 39003

    ENICNUMB           = 40001
    ENICWMAC           = 40002
    
errorcode = {
    E.EOK                :       [0x00000000,        "Test Pass"         ],
    E.EFAIL              :       [0x00000001,        "Test Fail"         ],
    E.EIO                :       [0x00000002,        "I/O error"         ],
    E.EEXIST             :       [0x00000003,        "Files not exists"  ],
    E.ESUPPORT           :       [0X00000004,        "Unsupported ops"   ],

    E.ELOGSEL            :       [0X00001000,        "Sel log have error message" ],
    E.ELOGSDR            :       [0X00001001,        "Sdr log have error message" ],
    E.ELOGDMESG          :       [0X00001002,        "Dmesg log have error message"],
    E.ELOGMCELOG         :       [0X00001003,        "Mcelog log have error message"],
    E.ELOGMESSAGE        :       [0X00001004,        "Message log have error message"],

    #E.ECPUCORE           :       [0X00002000,        "Cpu Core not match"],
    E.ECPUNUM            :       [0x00002001,        "Cpu Num not match" ],
    E.ECPUMHZ            :       [0x00002002,        "Cpu MHz not match" ],
    E.ECPUCORE           :       [0X00002003,        "Cpu Core not match"],
    E.ECPUNAME           :       [0X00002004,        "Cpu Name not match"],
    E.ECPUCACH           :       [0X00002005,        "Cpu L2_cache not match"],
    E.ECPUMCE            :       [0X00002006,        "Cpu mcelog includes error"],
    E.ECPUCODE           :       [0X00002007,        "Cpu Microcode check fail"],

    E.EMEMPRES           :       [0X00003001,        "Memory presence not match"],
    E.EMEMSIZE           :       [0X00003002,        "Memory size not match"],
    E.EMEMLOCA           :       [0X00003003,        "Memory locator not match"],
    E.EMEMTYPE           :       [0X00003004,        "Memory type not match"],
    E.EMEMSPEE           :       [0X00003005,        "Memory speed not match"],
    E.EMEMMANU           :       [0X00003006,        "Memory manufacturer not match"],
    E.EMEMPART           :       [0X00003007,        "Memory part number not match"],
    E.EMEMTEST           :       [0X00003008,        "Memory RW test fail"],
    E.EMEMECCE           :       [0X00003009,        "Memory ECC check fail"],
    E.EMEMMARG           :       [0X00003010,        "Memory Margin test fail"],

    E.ESSDNAME           :       [0x00004000,        "Ssd Name not match"],
    E.ESSDNUM            :       [0x00004001,        "Ssd Number not match"],
    E.ESSDSIZE           :       [0x00004002,        "Ssd Size not match"],
    E.ESSDMODEL          :       [0x00004003,        "Ssd Model not match"],
    E.ESSDDEVICE         :       [0x00004004,        "Ssd device name get fail"],
    E.ESSDHEALTH         :       [0x00004005,        "Ssd Smart Info check fail"],
    E.ESSDIOPS           :       [0x00004006,        "Ssd iops is lower than standard"],
    E.ESSDSPEED          :       [0x00004007,        "Ssd speed is lower than standard"],

    E.EVERSIONBMCMAIN    :       [0X00005000,        "Check bmc main version fail"],
    E.EVERSIONBMCBACKUP  :       [0X00005001,        "Check bmc backup version fail"],
    E.EVERSIONBMC        :       [0X00005002,        "Check bmc version fail"],
    E.EVERSIONBIOS       :       [0X00005003,        "Check bios version fail"],
    E.EVERSIONCPLDMAIN   :       [0X00005004,        "Check cpld main version fail"],
    E.EVERSIONCPLDBACKUP :       [0X00005005,        "Check cpld backup version fail"],
    E.EVERSIONCPLDHDD    :       [0X00005006,        "Check cpld HDD version fail"],
    E.EVERSIONI210       :       [0X00005007,        "Check I210 version fail"],
    E.EVERSIONI350       :       [0X00005008,        "Check I350 version fail"],
    E.EVERSIONMT2770     :       [0X00005009,        "Check MT2770 version fail"],
    E.EVERSIONPSU        :       [0X00005010,        "Check psu version fail"],
    E.EVERSIONPSUHW      :       [0X00005011,        "Check psu hw version fail"],
    E.EVERSIONPSUSW      :       [0x00005012,        "Check psu fw version fail"],
    E.EVERSIONEXPANDER   :       [0X00005013,        "Check expander version fail"],
    E.EVERSIONHDD        :       [0X00005014,        "Check HDD version fail"],
    E.EVERSIONVR         :       [0X00005015,        "Check VR version fail"],
    E.EVERSIONRAID       :       [0X00005016,        "Check raid version fail"],
    E.EVERSIONRAIDFW     :       [0X00005017,        "Check raid fw version fail"],
    E.EVERSIONRAIDBIOS   :       [0X00005018,        "Check raid biso version fail"],
    E.EVERSIONREIGN      :       [0X00005019,        "Nic firmware version not in place"],
    E.EVERSIONCPLD12BP   :       [0X00005020,        "Check cpld 12 bp version fail"],
    E.EVERSIONCPLD4BP    :       [0X00005021,        "Check cpld 4 bp version fail"],

    E.EFRUREAD           :       [0X00007001,        "FRU read fail"],
    E.EDMISYST           :       [0X00007002,        "Check system info fail"],
    E.EDMIBASE           :       [0X00007003,        "Check baseboard info fail"],
    E.EFRUPROG           :       [0X00007004,        "FRU 0 program fail"],
    E.EFRURISE           :       [0X00007005,        "FRU 11~12 program fail"],
    E.EFRUFANS           :       [0X00007006,        "FRU 3~8 program fail"],
    E.EFRUBMCM           :       [0X00007007,        "BMC Mac address uncorrect"],

    E.EPCIECARDNUM       :       [0X00008000,        "PCIE Card Num Invalid"],
    E.EPCIECARDUNMATCH   :       [0X00008001,        "PCIE Card Data Unmatch"],

    E.ERTCSET            :       [0X00013000,        "Set rtc fail"],
    E.ERTCCHECK          :       [0X00013001,        "Check rtc fail"],

    E.EUARTOPEN          :       [0X00015001,        "Uart open fail"],
    E.EUARTDATA          :       [0x00015002,        "Uart recv fail"],

    E.EVAGTEST           :       [0x00016001,        "Vga test fail"],

    E.EI2CNODEV          :       [0x00017001,        "I2c dev scan fail"],

    E.ERTCBAT            :       [0x00018001,        "Rtc battery test fail"],

    E.EPSUREIGN          :       [0X000019000,       "Psu not in place"],
    E.EPSUMODEL          :       [0X000019001,       "Check psu model fail"],
    E.EPSUTEMP           :       [0X000019002,       "Check psu temperature fail"],
    E.EPSUNUM            :       [0X000019003,       "Check psu num fail"],
    E.EPSUSTATUS         :       [0X000019004,       "Check psu status fail"],
    E.EPSUTEMPNC         :       [0X000019005,       "Psu temperature is slightly higher or low,but nothing serious"],
    E.EPSUTEMPCR         :       [0X000019006,       "Psu temperature is too high or very low and very serious"],
    E.EPSUTEMPNA         :       [0X000019007,       "Psu temperature is unknown and irrecoverable"],
    E.EPSUINSERTION      :       [0x000019008,       "Psu insertion is error"],

    E.EFANPRESENT        :       [0x00020001,        "Fan not present fail"],
    E.EFANPWM            :       [0x00020002,        "Fan set pwm fail"],

    E.ELOGCLEAR          :       [0X000027000,       " clear log fail"],

    E.ENICNUMB           :       [0X00040001,        "NIC number not match"],
    E.ENICWMAC           :       [0X00040002,        "NIC write mac fail"]
}