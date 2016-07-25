import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os

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

		optionList = ('8976', '8909', '8939')
		self.v = tk.StringVar()
		self.v.set(optionList[0])
		self.platformOpt = tk.OptionMenu(self, self.v, *optionList)
		self.platformOpt.grid(row=4, column=1, sticky=tk.W)
		
		self.startBtn = tk.Button(self, text="START", command=self.start)
		self.startBtn.grid(row=5, columnspan=2)

		
	def openVmDir(self):
		self.pathname=tkFileDialog.askdirectory()
		self.vmPath.delete(1.0)
		self.vmPath.insert(1.0, os.path.realpath(self.pathname))

	def openLogDir(self):
		self.pathname=tkFileDialog.askdirectory()
		self.logPath.delete(1.0)
		self.logPath.insert(1.0, os.path.realpath(self.pathname))
	
	def start(self):
		if self.vmPath.get(1.0) == "\n":
			tkMessageBox.showwarning("Warning", "vmlinux path not set")
			return
			
		if self.logPath.get(1.0) == "\n":
			tkMessageBox.showwarning("Warning", "Ram dump log path not set")
			return

		vmPath = os.path.realpath(self.vmPath.get(1.0,tk.END).split("\n")[0])
		logPath = os.path.realpath(self.logPath.get(1.0,tk.END).split("\n")[0])
		#print "checkDump.bat {0} {1} {2}".format(vmPath, logPath, self.v.get())
		os.system("checkDump.bat {0} {1} {2}".format(vmPath, logPath, self.v.get()))

		
app = Application() 
app.master.title('Check Dump GUI tool') 
app.mainloop() 