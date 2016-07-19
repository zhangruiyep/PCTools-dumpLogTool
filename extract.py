import sys
import os
import ConfigParser
import findFile

'''
extractTools = [
	[r"7-zip", r"7z.exe", r" x {0} -y -r -o{1}", r"C:\Progra~1\7-Zip"],
	[],
	[]
]
'''

class extractTool:
	def __init__(self, name, userPath=""):
		self.name = name
		self.exe = ""
		self.Path = userPath
		self.command = ""
		if self.check(userPath) < 0:
			print "ERR: %s invalid." % self.name
			self.valid = False
		else:
			print "%s init done." % self.name
			self.valid = True

	def check(self, userPath):
		cf = ConfigParser.ConfigParser()
		cf.read(os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini"))
		
		exeValue = cf.get(self.name, "Exe")
		if exeValue != "":
			self.exe = exeValue
			self.Path = cf.get(self.name, "Path")
			self.command = " "+cf.get(self.name, "Cmd")
		'''			
		for t in extractTools:
			#print t, self.name
			if t[0] == self.name:
				#print "got %s" % t[0]
				self.exe = t[1]
				self.command = t[2]
				if userPath == "":
					self.Path = t[3]
				else:
					self.Path = userPath
				break
		'''
		if self.exe == "":
			print self.name,"Not supported"
			return -1
			
		#print "checking %s..." % self.name
		files = findFile.findFilePath(self.exe, self.Path)
		if len(files) == 0:
			#print "%s not found" % self.name
			return -1			
		elif len(files) == 1:
			#print "got %s at %s" % (self.name, os.path.dirname(files[0]))
			self.exe = files[0]
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

		