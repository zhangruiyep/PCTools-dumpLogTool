import os
import sys
import cfg
import winRegistry
import findFile

class cygwinTool():
	def __init__(self):
		self.path = ""
		self.regPath = ""
		self.regName = ""
		self.binPath = ""
		if self.check() < 0:
			print "ERR: cygwin invalid."
			self.valid = False
		else:
			#print "cygwin init done."
			self.valid = True
	
	def getPath(self):
		if self.valid == True:
			#print self.binPath
			return self.binPath
		else:
			return ""

	def check(self):
		self.cfg = cfg.configFile()
		cf = self.cfg.cp
		
		try:
			self.path = cf.get("cygwin", "Path")
		except:
			pass

		try:
			self.regPath = cf.get("cygwin", "RegPath")
			self.regName = cf.get("cygwin", "RegName")
		except:
			pass

		if self.regPath != "":
			pathInReg = winRegistry.getRegValue(self.regPath, self.regName)[0]

		''' Now we have path in registry and user define path in ini file.
		Check user path first.
		If user path is invalid, then check registry and update user path in ini for next time. '''
		binPath = os.path.join(self.path, r"bin")
		#print binPath
		files = findFile.findFilePath(r"cygwin1.dll", binPath)
		if len(files) == 0:
			# check regitry path
			#print "%s not found" % self.name
			#print "pathInReg=%s" % pathInReg
			binPath = os.path.join(pathInReg, r"bin")
			files = findFile.findFilePath(r"cygwin1.dll", binPath)
			if len(files) == 0:
				return -1
			elif len(files) == 1:
				self.binPath = os.path.realpath(binPath)
				cf.set("cygwin", "Path", pathInReg)
				
				self.cfg.write()
				
				return 0
		elif len(files) == 1:
			self.binPath = os.path.realpath(binPath)
			return 0

