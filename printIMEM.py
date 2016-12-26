''' Change list:
2016-03-29 init version, only support PMI8952
2016-10-14 complete 8 PON registors
'''
import sys
import os

decode = {
	"23":"Secure watchdog bite",
	"13":"PMIC abnormal reset",
	"1B":"TSENSE reset (temperature sensor-triggered reset)",
	"4":"Software triggered reset",
	"0":"Non-MSM triggered reset",
	}

def printRESET(filename):
	f = open(filename, "rb")
	#print filename, "is opened"
	# offset to GCC_RESET_STATUS
	f.seek(0x764,0)
	byte = f.read(1)
	value = byte.encode("hex")
	
	logf = open(os.path.join(os.path.split(os.path.realpath(filename))[0], r"parser\GCC_RESET_STATUS"), "wb")
	print "0x"+value
	logf.write("0x"+value+"\n")
	try:
		print decode[value]
		logf.write (decode[value])
	except:
		print "unknown reason"
		logf.write ("unknown reason\n")
	
	logf.close()
	
	f.close()
