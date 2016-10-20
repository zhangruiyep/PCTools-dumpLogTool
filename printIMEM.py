''' Change list:
2016-03-29 init version, only support PMI8952
2016-10-14 complete 8 PON registors
'''
import sys

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
	print "0x"+value
	try:
		print decode[value]
	except:
		print "unknown reason"
	
	f.close()
