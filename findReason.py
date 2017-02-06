import os
import cfg

'''
reasons = [
	"Kernel panic",
	"Watchdog bark",
	"Unable to handle kernel paging request",
	]
'''

def findReason(filename):
	result = ""

	c = cfg.configFile()
	cf = c.cp
	keys = cf.get("Reason", "Keywords")
	#print keys
	reasons = keys.split(';')
	#print reasons
	print "=================="
	print "Finding reasons..."
	f = open(filename, "r")
	for l in f.readlines():
		for r in reasons:
			if r in l:
				print l
				if r == "vmlinux is probably wrong":
					result = r
	f.close()
	
	print "That's all I can find..."
	
	return result
	
