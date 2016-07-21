import os
import sys
import ConfigParser
import findFile
import extract
import findReason

# main
if len(sys.argv) < 3 or len(sys.argv) > 4:
	print "Usage: \tcheckDump vmlinux_path dump_log_path [MSM_platform]"
	print "Ver: \t1.02 2016-07-13"
else:
	# find all files we need
	vmPath = findFile.extractFind("vmlinux", sys.argv[1])
	logPath = findFile.extractFind("DDRCS0.BIN", sys.argv[2])
	# read ramdump path from cfg.ini
	thisPath = os.path.split(os.path.realpath(__file__))[0]
	cf = ConfigParser.ConfigParser()
	cf.read(os.path.join(thisPath,"cfg.ini"))
	#print cf.sections()
	lpPath = os.path.split(thisPath)[0]
	
	#print lpPath
	parserPath = findFile.extractFind("ramparse.py", os.path.realpath(lpPath))
	
	# get platform info
	if len(sys.argv) > 3:
		platform = sys.argv[3]
	else:
		platform = ""
	
	arch = "64-bit"
	if platform != "":
		arch = cf.get(platform, "arch")
		fhCmd = " --force-hardware "+platform
	else:
		fhCmd = ""
	
	nm = cf.get(arch, "nm")
	gdb = cf.get(arch, "gdb")
	lpCmd = cf.get("LinuxParser", "Cmd")

	parserCmdLine = r"c:\Python27\python {0}\ramparse.py {1} -v {2}\vmlinux -a {3} -o {3}\parser {4} --nm-path={0}\{5} --gdb-path={0}\{6} --{7}".format(parserPath, lpCmd, vmPath, logPath, fhCmd, nm, gdb, arch)
	
	if vmPath != "" and logPath != "":
		print "set vmlinux path: %s\nset log path: %s" % (vmPath, logPath)
		print "set platform: %s" % platform
		
		# call ramparse.py
		#print parserCmdLine
		os.system(parserCmdLine)
		
		findReason.findReason(os.path.join(logPath, r"parser\dmesg_TZ.txt"))
	else:
		print "ERR: log or vmlinux path can not found! STOP"
	