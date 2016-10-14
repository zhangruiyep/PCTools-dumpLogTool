''' Change list:
2016-03-29 init version, only support PMI8952
2016-10-14 complete 8 PON registors
'''
import sys

def printRESET(filename):
	f = open(filename, "rb")
	#print filename, "is opened"
	# offset to GCC_RESET_STATUS
	f.seek(0x764,0)
	byte = f.read(1)
	print "0x"+byte.encode("hex")
	
	f.close()
