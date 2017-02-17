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
		decompressed_files = []
		pkgs = findPkg(pkgTypes, rootdir)
		need_extract_files = [x for x in pkgs if x not in decompressed_files] + [x for x in decompressed_files if x not in pkgs]
		while need_extract_files != []:
			#print "found pkgs need extract:"
			print need_extract_files
			
			if len(need_extract_files) == 0:
				#print "pkgs not found"
				return None
			else:
				#print need_extract_files
				for p in need_extract_files:
					arch = compressTool.extractFile(p, toolName)
					if arch.extractFile() == 0:
						decompressed_files.append(p)
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
						
			pkgs = findPkg(pkgTypes, rootdir)
			need_extract_files = [x for x in pkgs if x not in decompressed_files] + [x for x in decompressed_files if x not in pkgs]
	else:
		# only get one file, return it
		return file
	
