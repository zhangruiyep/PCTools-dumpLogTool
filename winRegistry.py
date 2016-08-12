import _winreg
import os

def getRegValue(regPath, regName):

	#print regPath, regName
	value = ""
	
	try:
		proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
		proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
	except:
		pass

	if proc_arch == 'x86' and not proc_arch64:
		arch_keys = {0}
	elif proc_arch == 'x86' or proc_arch == 'amd64':
		arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
	else:
		raise Exception("Unhandled arch: %s" % proc_arch)

	for arch_key in arch_keys:
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regPath, 0, _winreg.KEY_READ | arch_key)
			value = _winreg.QueryValueEx(key, regName)
			#print arch_key, value
		except OSError:
			#print OSError.errno
			pass
	
	return value