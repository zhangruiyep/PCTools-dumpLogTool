import os
import fnmatch
import cfg
import compressTool

def findFile(filename):
	results = []
	for file in os.listdir("."):
		if fnmatch.fnmatch(file, filename):
			#print "found "+file
			results.append(file)
	return results

def findFilePath(filename, rootdir):
	result = []
	#print rootdir
	for root, subFolders, files in os.walk(rootdir):
		#print root, subFolders, files
		for f in files:  
			if fnmatch.fnmatch(f, filename):  
				result.append(os.path.join(root, f)) 
	return result 
	
def findPkg(filenames, rootdir):
	#print filenames, rootdir
	result = []
	for root, subFolders, files in os.walk(rootdir):
		#print root, subFolders, files
		for f in files:
			for filename in filenames:  
				if fnmatch.fnmatch(f, filename):  
					result.append(os.path.join(root, f)) 
	return result 

def findOneFile(filename, rootdir):
	files = findFilePath(filename, rootdir)
	if len(files) == 1:
		return os.path.dirname(files[0])
	elif len(files) == 0:
		return None
	else:
		return "multi"	
		
	
def extractFind(filename, rootdir):
	result = []
	file = findOneFile(filename, rootdir)
	if file == "multi":
		# get multi file, no need to extract
		print "Find multi files with same name. Please change path to choose one."
		return None
	elif file == None:
		# need extract then find
		print "%s not found" % filename
		
		print "maybe it is in archive..."

		c = cfg.configFile()
		cf = c.cp

		toolName = cf.get("Tool", "Name")
		FileTypes = cf.get("Tool", "FileTypes")
		
		pkgTypes = FileTypes.split(';')
		# find archive and extract
		pkgs = findPkg(pkgTypes, rootdir)
		if len(pkgs) == 0:
			#print "pkgs not found"
			return None
		else:
			print pkgs
			for p in pkgs:
				arch = compressTool.extractFile(p, toolName)
				if arch.extractFile() == 0:
					file = findOneFile(filename, rootdir)
					if file == "multi":
						print "Find multi files with same name. Please change path to choose one."
						return None
					elif file == None:
						pass
					else:
						return file
				else:
					print "ERR: %s format err" % p
					pass

		# pkg may be double archived, like .tar.gz
		# check for new archive
		pkgs2 = findPkg(pkgTypes, rootdir)
		for p in pkgs2:
			if p not in pkgs:
				arch = compressTool.extractFile(p, toolName)
				if arch.extractFile() == 0:
					file = findOneFile(filename, rootdir)
					if file == "multi":
						print "Find multi files with same name. Please change path to choose one."
						return None
					elif file == None:
						pass
					else:
						return file
				else:
					print "ERR: %s format err" % p
					pass
		
	else:
		# only get one file, return it
		return file
	
