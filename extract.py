import sys
import os
import ConfigParser
import findFile
import winRegistry

class extractTool:
	def __init__(self, name, userPath=""):
		self.name = name
		self.exe = ""
		self.Path = userPath
		self.command = ""
		self.RegPath = ""
		self.RegName = ""
		if self.check(userPath) < 0:
			print "ERR: %s invalid." % self.name
			self.valid = False
		else:
			print "%s init done." % self.name
			self.valid = True

	def check(self, userPath):
		cf = ConfigParser.ConfigParser()
		iniFileName = os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini")
		cf.read(iniFileName)
		
		exeValue = cf.get(self.name, "Exe")
		if exeValue != "":
			self.exe = exeValue
			self.command = " "+cf.get(self.name, "Cmd")
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
			print "pathInReg=%s" % pathInReg
			files = findFile.findFilePath(self.exe, pathInReg)
			if len(files) == 0:
				return -1
			elif len(files) == 1:
				self.exe = '"{}"'.format(os.path.realpath(files[0]))
				cf.set(self.name, "Path", pathInReg)
				
				f = open(iniFileName, "w")
				cf.write(f)
				f.close()
				
				return 0
		elif len(files) == 1:
			#print "got %s at %s" % (self.name, os.path.dirname(files[0]))
			self.exe = '"{}"'.format(os.path.realpath(files[0]))
			return 0


class archive:
	def __init__(self, fileName, toolName):
		self.fileNm = fileName
		self.tool = extractTool(toolName)
	
	def extractFile(self):
		if self.tool.valid == False:
			return -1
		else:
			print self.tool.exe + self.tool.command.format(self.fileNm, os.path.dirname(self.fileNm))
			os.system(self.tool.exe + self.tool.command.format(self.fileNm, os.path.dirname(self.fileNm)))
			return 0

		