import os
import ConfigParser

'''
reasons = [
	"Kernel panic",
	"Watchdog bark",
	"Unable to handle kernel paging request",
	]
'''

def findReason(filename):
	cf = ConfigParser.ConfigParser()
	cf.read(os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini"))
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
	f.close()
	
	print "That's all I can find..."