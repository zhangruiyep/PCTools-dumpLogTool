import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
import ConfigParser
import checkDump
import pack
import findFile

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master) 
		self.grid() 
		self.createWidgets()
		
	def createWidgets(self):
		self.vmInfo = tk.Label(self, text="Choose vmlinux path:(space char or Chinese NOT supported)", justify=tk.LEFT)
		self.vmInfo.grid(row=2, sticky=tk.W, columnspan=2)
	
		self.vmPath = tk.Text(self, height = 1, width = 40)
		self.vmPath.grid(row=3)

		self.getVmBtn = tk.Button(self, text="Open", command=self.openVmDir, width=10)
		self.getVmBtn.grid(row=3, column=1)

		self.vmInfo = tk.Label(self, text="Choose ram dump log path:(space char or Chinese NOT supported)", justify=tk.LEFT)
		self.vmInfo.grid(row=0, sticky=tk.W, columnspan=2)
		
		self.logPath = tk.Text(self, height = 1, width = 40)
		self.logPath.grid(row=1)

		self.getLogBtn = tk.Button(self, text="Open", command=self.openLogDir, width=10)
		self.getLogBtn.grid(row=1, column=1)
		
		self.vmInfo = tk.Label(self, text="Choose hardware platform:", justify=tk.LEFT)
		self.vmInfo.grid(row=4, sticky=tk.W)

		optionList = self.getOptions()
		self.v = tk.StringVar()
		self.v.set(optionList[0])
		self.platformOpt = tk.OptionMenu(self, self.v, *optionList)
		self.platformOpt.grid(row=4, column=1, sticky=tk.W)
		
		self.startBtn = tk.Button(self, text="START", command=self.start)
		self.startBtn.grid(row=5, columnspan=2)
		
		self.packBtn = tk.Button(self, text="Pack Parser Result", command=self.packResult)
		self.packBtn.grid(row=6)

		self.packBtn = tk.Button(self, text="Pack All", command=self.packAll)
		self.packBtn.grid(row=6, column=1)
		

	def getOptions(self):
		optionList = []
		thisPath = os.path.split(os.path.realpath(__file__))[0]
		cf = ConfigParser.ConfigParser()
		cf.read(os.path.join(thisPath,"cfg.ini"))
		
		for sec in cf.sections():
			if "arch" in cf.options(sec):
				optionList.append(sec)
		
		return optionList
		
	def openVmDir(self):
		self.pathname=tkFileDialog.askdirectory()
		self.vmPath.delete(1.0, tk.END)
		self.vmPath.insert(1.0, os.path.realpath(self.pathname))

	def openLogDir(self):
		self.pathname=tkFileDialog.askdirectory()
		self.logPath.delete(1.0, tk.END)
		self.logPath.insert(1.0, os.path.realpath(self.pathname))
	
	def getPathFromText(self, textWidget):
		if textWidget.get(1.0) != "\n":
			return os.path.realpath(textWidget.get(1.0,tk.END).split("\n")[0])
		else:
			return None
	
	def start(self):
		realVmPath = self.getPathFromText(self.vmPath)
		if realVmPath == None:
			tkMessageBox.showwarning("Warning", "vmlinux path not set")
			return
		
		realLogPath = self.getPathFromText(self.logPath)
		if realLogPath == None:
			tkMessageBox.showwarning("Warning", "Ram dump log path not set")
			return
			
		#print "checkDump.bat {0} {1} {2}".format(vmPath, logPath, self.v.get())
		#os.system("checkDump.bat {0} {1} {2}".format(realVmPath, realLogPath, self.v.get()))
		checkDump.checkDump(realVmPath, realLogPath, self.v.get())

	def pack(self, option):
		txtVmPath = self.getPathFromText(self.vmPath)
		if txtVmPath == None:
			tkMessageBox.showwarning("Warning", "vmlinux path not set")
			return
		
		txtLogPath = self.getPathFromText(self.logPath)
		if txtLogPath == None:
			tkMessageBox.showwarning("Warning", "Ram dump log path not set")
			return

		cf = ConfigParser.ConfigParser()
		cf.read(os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini"))
		toolName = cf.get("Tool", "Name")

		realLogPath = findFile.extractFind("DDRCS0.BIN", txtLogPath)
		p = pack.packFiles(realLogPath + "\\parser\\", toolName)
		p.packFiles()

		if option == "all":
			p = pack.packFiles(realLogPath + "\\", toolName, "dump")
			p.packFiles()
			
			realVmPath = findFile.extractFind("vmlinux", txtVmPath)
			p = pack.packFiles(realVmPath + "\\vmlinux", toolName)
			p.packFiles()
		
	def packResult(self):
		self.pack("result")
	
	def packAll(self):
		self.pack("all")
		
		
app = Application() 
app.master.title('Check Dump GUI tool') 
app.mainloop() 