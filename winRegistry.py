import _winreg
import os

def getRegValue(regPath, regName):

	#print regPath, regName
	value = ""
	proc_arch64 = None
	
	try:
		proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
		proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
	except:
		pass

	#print proc_arch
	#print proc_arch64
	if proc_arch == 'x86' and proc_arch64 == None:
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regPath, 0, _winreg.KEY_READ)
			value = _winreg.QueryValueEx(key, regName)
		except OSError:
			print OSError.errno
			pass

	elif proc_arch == 'x86' or proc_arch == 'amd64':
		arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
		for arch_key in arch_keys:
			try:
				key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regPath, 0, _winreg.KEY_READ | arch_key)
				value = _winreg.QueryValueEx(key, regName)
				print arch_key, value
			except OSError:
				print OSError.errno
				pass
	else:
		raise Exception("Unhandled arch: %s" % proc_arch)

	
	return value
