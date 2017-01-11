import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
import checkDump
import compressTool
import findFile
import cfg

class inputFrame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidget()
		
	def createWidget(self):
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
	
	def setWidgetText(self, txtWidget):
		pathname=tkFileDialog.askdirectory()
		txtWidget.delete(1.0, tk.END)
		txtWidget.insert(1.0, os.path.realpath(pathname))

	def openVmDir(self):
		self.setWidgetText(self.vmPath)
		
	def openLogDir(self):
		self.setWidgetText(self.logPath)
		
	def getOptions(self):
		return self.master.cfg.getPlatformOptions()

class actFrame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidget()
		
	def createWidget(self):
		self.startBtn = tk.Button(self, text="START", command=self.start)
		self.startBtn.grid(row=0, columnspan=2, sticky=tk.W+tk.E)
		
		self.packBtn = tk.Button(self, text="Pack Parser Result", command=self.packResult, width=20)
		self.packBtn.grid(row=1)

		self.packBtn = tk.Button(self, text="Pack All", command=self.packAll, width=20)
		self.packBtn.grid(row=1, column=1)

	
	def start(self):
		realVmPath = self.master.updateVmPath()
		if realVmPath == None:
			tkMessageBox.showwarning("Warning", "vmlinux path not set")
			return
		
		realLogPath = self.master.updateLogPath()
		if realLogPath == None:
			tkMessageBox.showwarning("Warning", "Ram dump log path not set")
			return
		
		realPlatform = self.master.updatePlatform()
		#print "checkDump.bat {0} {1} {2}".format(vmPath, logPath, self.v.get())
		checkDump.checkDump(realVmPath, realLogPath, realPlatform)

	def pack(self, option):
		txtVmPath = self.master.updateVmPath()
		if txtVmPath == None:
			tkMessageBox.showwarning("Warning", "vmlinux path not set")
			return
		
		txtLogPath = self.master.updateLogPath()
		if txtLogPath == None:
			tkMessageBox.showwarning("Warning", "Ram dump log path not set")
			return

		toolName = self.master.cfg.cp.get("Tool", "Name")

		realLogPath = findFile.extractFind("DDRCS0.BIN", txtLogPath)
		p = compressTool.packFiles(realLogPath + "\\parser\\", toolName)
		p.packFiles()

		if option == "all":
			p = compressTool.packFiles(realLogPath + "\\", toolName, "dump")
			p.packFiles()
			
			realVmPath = findFile.extractFind("vmlinux", txtVmPath)
			p = compressTool.packFiles(realVmPath + "\\vmlinux", toolName, "vmlinux")
			p.packFiles()
		
	def packResult(self):
		self.pack("result")
	
	def packAll(self):
		self.pack("all")

		
		
class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master) 
		self.vmPath = ""
		self.logPath = ""
		self.platform = ""
		self.cfg = cfg.configFile()
		self.grid() 
		self.createFrames()
	
	def createFrames(self):
		self.inputFrame = inputFrame(self)
		self.actFrame = actFrame(self)

	def getPathFromText(self, textWidget):
		if textWidget.get(1.0) != "\n":
			return os.path.realpath(textWidget.get(1.0,tk.END).split("\n")[0])
		else:
			return None
		
	def updateVmPath(self):
		self.vmPath = self.getPathFromText(self.inputFrame.vmPath)
		return self.vmPath

	def updateLogPath(self):
		self.logPath = self.getPathFromText(self.inputFrame.logPath)
		return self.logPath
		
	def updatePlatform(self):
		self.platform = self.inputFrame.v.get()
		return self.platform
		
app = Application() 
app.master.title('Check Dump GUI tool') 
app.mainloop() 