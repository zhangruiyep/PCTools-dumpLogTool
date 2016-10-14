''' Change list:
2016-03-29 init version, only support PMI8952
2016-10-14 complete 8 PON registors
'''
import sys
import struct

class PONregister(object):
        def __init__(self, name, bitsList):
                self.name = name
                self.bitsList = bitsList
        def printAll(self):
                print self.name
                for i in range(0, 8):
                        print self.bitsList[i][0]
        def printValue(self, value):
                if self.name != "dummy":
                        print self.name
                        for i in range(0, 8):
                                bit = value & 0x01
                                if bit == 1:
                                        print self.bitsList[i][1]
                                value = value >> 1
                        print ""
        


PON_PON_REASON1_tbl = [
  	["HARD_RESET",  "Triggered from a Hard Reset event (check POFF reason for the trigger)"],
  	["SMPL",        "Triggered from SMPL"],
  	["RTC",         "Triggered from RTC"],
  	["DC_CHG",      "Triggered from DC charger"],
  	["USB_CHG",     "Triggered from USB charger"],
  	["PON1",        "Triggered from PON1"],
  	["CBLPWR_N",    "Triggered from CBL_PWR1_N"],
  	["KPDPWR_N",    "Triggered from new KPDPWR press"]
]

PON_PON_REASON1 = PONregister("PON_PON_REASON1", PON_PON_REASON1_tbl)

dummy_tbl = []
DUMMY = PONregister("dummy", dummy_tbl) 

PON_WARM_RESET_REASON1_tbl = [
    ["SOFT",    "Triggered by Software"],
    ["PS_HOLD", "Triggered by PS_HOLD"],
    ["PMIC_WD", "Triggered by PMIC Watchdog"],
    ["GP1",     "Triggered by Keypad_Reset1"],
    ["GP2",     "Triggered by Keypad_Reset2"],
    ["KPDPWR_AND_RESIN",    "Triggered by simultaneous KPDPWR_N + RESIN_N"],
    ["RESIN_N",     "Triggered by RESIN_N"],
    ["KPDPWR_N",    "Triggered by KPDPWR_N"],
]

PON_WARM_RESET_REASON1 = PONregister("PON_WARM_RESET_REASON1", PON_WARM_RESET_REASON1_tbl)

PON_WARM_RESET_REASON2_tbl = [
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    ["AFP",     "Triggered AFP"],
    ["", ""],
    ["", ""],
    ["", ""],
]

PON_WARM_RESET_REASON2 = PONregister("PON_WARM_RESET_REASON2", PON_WARM_RESET_REASON2_tbl)

PON_POFF_REASON1 = PONregister("PON_POFF_REASON1", PON_WARM_RESET_REASON1_tbl)

PON_POFF_REASON2_tbl = [
    ["",    ""],
    ["", ""],
    ["AVDD_RB", "Triggered by AVDD_RB"],
    ["CHARGER",     "Triggered by Charger (ENUM_TIMER, BOOT_DONE)"],
    ["AFP",     "Triggered AFP"],
    ["UVLO",    "Triggered by UVLO"],
    ["OTST3",     "Triggered by Overtemp"],
    ["STAGE3",    "Triggered by stage3 reset"],
]

PON_POFF_REASON2 = PONregister("PON_POFF_REASON2", PON_POFF_REASON2_tbl)

PON_SOFT_RESET_REASON1 = PONregister("PON_SOFT_RESET_REASON1", PON_WARM_RESET_REASON1_tbl)
PON_SOFT_RESET_REASON2 = PONregister("PON_SOFT_RESET_REASON2", PON_WARM_RESET_REASON2_tbl)


PMI8952_PON = [
        PON_PON_REASON1,
        DUMMY,
        PON_WARM_RESET_REASON1,
        PON_WARM_RESET_REASON2,
        PON_POFF_REASON1,
        PON_POFF_REASON2,
        PON_SOFT_RESET_REASON1,
        PON_SOFT_RESET_REASON2,
                ]


def printUsage():
	print "Usage: printPON.py filename hardwareType"
	print "Ver: 20160329"

def checkHwType(hwType):
	if hwType != "PMI8952":
	        return False
	else:
	        return True

def printPON(filename, hwType):
	if checkHwType(hwType) == False:
		print hwType+" is not supported."
		return
	f = open(filename, "rb")
	#print filename, "is opened"
	for i in range(0,8):
	  curChar = struct.unpack("B", f.read(1))[0]
	  #print curChar
	  PMI8952_PON[i].printValue(curChar)
		
	f.close()
'''
# main

if len(sys.argv) != 3:
	printUsage()
else:
	printPON(sys.argv[1], sys.argv[2])
'''