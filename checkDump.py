import os
import sys
import findFile
import findReason
import printPON
import printIMEM
from cfg import *
import cygwin

def checkDump(vm_path, log_path, platform):
	# read ramdump path from cfg.ini
	thisPath = os.path.split(os.path.realpath(__file__))[0]
	lpPath = os.path.split(thisPath)[0]
	cfg = configFile()
	cf = cfg.cp
	
	parserPath = findFile.extractFind("ramparse.py", os.path.realpath(lpPath))
	
	# find all files we need
	vmPath = findFile.extractFind("vmlinux", vm_path)
	logPath = findFile.extractFind("DDRCS0.BIN", log_path)

	arch = "64-bit"
	if platform == "":
		fhCmd = ""
	elif "unknown" in platform:
		arch = cf.get("arch", platform)
		fhCmd = ""
	else:
		arch = cf.get("arch", platform)
		fhCmd = " --force-hardware "+platform
	
	nm = cf.get(arch, "nm")
	gdb = cf.get(arch, "gdb")
	lpCmd = cf.get("LinuxParser", "Cmd")

	parserCmdLine = r"c:\Python27\python {0}\ramparse.py {1} -v {2}\vmlinux -a {3} -o {3}\parser {4} --nm-path={0}\{5} --gdb-path={0}\{6} --{7}".format(parserPath, lpCmd, vmPath, logPath, fhCmd, nm, gdb, arch)
	
	if vmPath != None and logPath != None:
		print "set vmlinux path: %s\nset log path: %s" % (vmPath, logPath)
		print "set platform: %s" % platform
		
		# call ramparse.py
		print parserCmdLine
		os.system(parserCmdLine)
		
		result = findReason.findReason(os.path.join(logPath, r"parser\dmesg_TZ.txt"))

		cyg = cygwin.cygwinTool()
		cygPath = cyg.getPath()
		if cygPath != "" and result == "vmlinux is probably wrong":
			print "============================="
			print "Get Linux version in vmlinux:"
			grepCmdLine = r'{0}\strings {1}\vmlinux | {0}\grep "Linux version"'.format(cygPath, vmPath)
			#print grepCmdLine
			os.system(grepCmdLine)
			print "========================="
			print "Get Linux version in log:"
			grepCmdLine = r'{0}\strings {1}\DDRCS0.BIN | {0}\grep "Linux version"'.format(cygPath, logPath)
			#print grepCmdLine
			os.system(grepCmdLine)
		
		# check if extra ops exist
		ex = cf.get("LinuxParser", "extra")
		exops = ex.split(';')
		
		# check GCC_RESET_STATUS
		if "GCC_RESET_STATUS" in exops:
			print "======================"
			print "Dump GCC_RESET_STATUS:"		
			printIMEM.printRESET(os.path.join(logPath, "OCIMEM.BIN"))
		
		# check PMIC_PON
		if "PMIC_PON" in exops:
			print "=============="
			print "Dump PMIC_PON:"
			printPON.printPON(os.path.join(logPath, "PMIC_PON.BIN"), "PMI8952")
	else:
		print "ERR: log or vmlinux path can not found! STOP"


# main
if len(sys.argv) < 3 or len(sys.argv) > 4:
	print "Usage: \tcheckDump vmlinux_path dump_log_path [MSM_platform]"
else:
	# get input from sys.argv
	if len(sys.argv) > 3:
		pf = sys.argv[3]
	else:
		pf = ""

	checkDump(sys.argv[1], sys.argv[2], pf)
