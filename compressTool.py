import sys
import os
import findFile
import winRegistry
import datetime
from cfg import *

class compressTool():
	def __init__(self, name, userPath=""):
		self.name = name
		self.exe = ""
		self.Path = userPath
		self.RegPath = ""
		self.RegName = ""
		if self.check(userPath) < 0:
			print "ERR: %s invalid." % self.name
			self.valid = False
		else:
			print "%s init done." % self.name
			self.valid = True

	def check(self, userPath):
		self.cfg = configFile()
		cf = self.cfg.cp
		
		exeValue = cf.get(self.name, "Exe")
		if exeValue != "":
			self.exe = exeValue
			try:
				self.Path = cf.get(self.name, "Path")
			except:
				pass

			try:
				self.RegPath = cf.get(self.name, "RegPath")
				self.RegName = cf.get(self.name, "RegName")
			except:
				pass

		if self.exe == "":
			print self.name,"Not supported"
			return -1
			
		if self.RegPath != "":
			pathInReg = winRegistry.getRegValue(self.RegPath, self.RegName)[0]
			
		''' Now we have path in registry and user define path in ini file.
		Check user path first.
		If user path is invalid, then check registry and update user path in ini for next time. '''
		
		#print "checking %s..." % self.name
		files = findFile.findFilePath(self.exe, self.Path)
		if len(files) == 0:
			# check regitry path
			#print "%s not found" % self.name
			#print "pathInReg=%s" % pathInReg
			files = findFile.findFilePath(self.exe, pathInReg)
			if len(files) == 0:
				return -1
			elif len(files) == 1:
				self.exe = '"{}"'.format(os.path.realpath(files[0]))
				cf.set(self.name, "Path", pathInReg)
				
				self.cfg.write()
				
				return 0
		elif len(files) == 1:
			#print "got %s at %s" % (self.name, os.path.dirname(files[0]))
			self.exe = '"{}"'.format(os.path.realpath(files[0]))
			return 0

class extractTool(compressTool):
	def __init__(self, name, userPath=""):
		self.extractcmd = ""
		compressTool.__init__(self, name, userPath)
		if self.valid == True:
			if self.extractCheck() < 0:
				self.valid = False
			else:
				print "extractTool init done"
				self.valid = True
	
	def extractCheck(self):
		try:
			self.extractcmd = " "+self.cfg.cp.get(self.name, "extractcmd")
		except:
			return -1
			
		return 0

class extractFile:
	def __init__(self, fileName, toolName):
		self.fileNm = fileName
		self.tool = extractTool(toolName)
	
	def extractFile(self):
		if self.tool.valid == False:
			return -1
		else:
			print self.tool.exe + self.tool.extractcmd.format(self.fileNm, os.path.dirname(self.fileNm))
			os.system(self.tool.exe + self.tool.extractcmd.format(self.fileNm, os.path.dirname(self.fileNm)))
			return 0

		
class packTool(compressTool):
	def __init__(self, name, userPath=""):
		self.packCmd = ""
		self.packType = ""
		self.packLogCmd = ""
		compressTool.__init__(self, name, userPath)
		if self.valid == True:
			if self.checkpack() < 0:
				self.valid = False
			else:
				print "packTool init done"
				self.valid = True
	
	def checkpack(self):
		try:
			self.packCmd = " "+self.cfg.cp.get(self.name, "packCmd")
			self.packType = self.cfg.cp.get(self.name, "packType")
			self.packLogCmd = self.cfg.cp.get(self.name, "packLogCmd")
		except:
			return -1
		
		return 0

class packFiles:
	def __init__(self, fileName, toolName, option=""):
		self.fileNm = fileName
		self.option = option
		self.tool = packTool(toolName)
	
	def packFiles(self):
		if self.tool.valid == False:
			return -1
		else:
			if self.option == "dump":
				self.tool.packCmd += " "+self.tool.packLogCmd
			
			today = datetime.date.today()
			now = datetime.datetime.now()
			if self.option == "vmlinux":
				nowStr = ""
			else:
				nowStr = datetime.datetime.strftime(now, "_%Y%m%d_%H%M")
			print self.tool.exe + self.tool.packCmd.format(os.path.realpath(self.fileNm) + nowStr + "." + self.tool.packType, self.fileNm)
			os.system(self.tool.exe + self.tool.packCmd.format(os.path.realpath(self.fileNm) + nowStr + "." + self.tool.packType, self.fileNm))
			return 0
			