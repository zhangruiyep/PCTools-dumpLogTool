import os
import sys
import ConfigParser
import extract

class packTool(extract.extractTool):
	def __init__(self, name, userPath=""):
		self.packCmd = ""
		self.dftType = ""
		extract.extractTool.__init__(self, name)
		if self.valid == True:
			if self.checkpack() < 0:
				self.valid = False
			else:
				self.valid = True
	
	def checkpack(self):
		cf = ConfigParser.ConfigParser()
		iniFileName = os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini")
		cf.read(iniFileName)

		try:
			self.packCmd = " "+cf.get(self.name, "packCmd")
			self.dftType = cf.get(self.name, "dftType")
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
				self.tool.packCmd += " -xr!parser* -v200m"
				
			print self.tool.exe + self.tool.packCmd.format(os.path.realpath(self.fileNm) + "." + self.tool.dftType, self.fileNm)
			os.system(self.tool.exe + self.tool.packCmd.format(os.path.realpath(self.fileNm) + "." + self.tool.dftType, self.fileNm))
			return 0
	