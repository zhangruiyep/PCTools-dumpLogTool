Tools to make Linux parser easier to use.
=========================================
Feature:
--------
1. Find vmlinux and dump log in folder, then set the correct path.

2. If vmlinux or dump log is in archive, such as zip format, it will be extracted automatically. Then set the path.

3. You can pack result or log/vmlinux.

Usage:
------
1. Unzip this tool into ramdump tool. Such as D:\ramdump\dumpLogTool\start.bat

2. Modify ini file to your real path if needed.

3. Double click start.bat to run GUI.

4. Choose log path, vmlinux path and platform.

5. Click START button. It will open a console and show the result.

6. Click pack buttons to pack result or log if needed.

Note:
-----
1. Path or file name does not support Chinese or non-ASCII char.

2. Unzip tool only add 7-zip now. You can add your tool in ini file.

3. Vmlinux path or log path should NOT be a big folder which contains too many zip files. This tool will unzip them all and find the first match file.

Change History:
---------------
* 2016/7/12

	* The init version.

* 2016/7/13

	* Add cfg.ini. You can change tool or path in this file.

* 2016/7/13

	* Generate ramparse.py cmd line base on ini. Do not need dump.bat support. 

	* Remove some debug msg.

* 2016/7/15

	* Platform is an optional now. ramparse will automatic detect as default. But it does not work all the time. Set the platform is still recommanded.

	* Fix minor bugs.

* 2016/7/19

	* Add feature: find key words in dmesg. The key words is store in ini file.
	
* 2016/7/21

	* Get Linux Parser path base on current file path. Do not need modify in ini file.

	* Fix minor bugs.
	
* 2016/7/25

	* Add a simple tkinter GUI. Run start.bat.
	
	* Sperate checkdump function from main.
	
	* Add WinRAR support. NOT tested.
	
* 2016/7/27

	* Print msg modified.

* 2016/7/29

	* Add registry support. It will read install path from registry.

* 2016/8/10

	* GUI read platform options from ini.
	
* 2016/10/09

	* Improve .tar.gz support

* 2016/10/14

	* Add PMIC_PON GCC_RESET_STATUS info print.
	
* 2016/11/23

	* Hide unused info. Make info more clear.
	
* 2016/12/20

	* Add feature: package result
	
* 2016/12/26

	* Improve code struct to make it easier to read and mantain.
	
	* Improve GUI layout.
	
	* Imporve extract and find code flow to save time.
	
* 2017/1/11

	* Add cygwin support to print Linux version

* 2017/2/17

	* Add "while" for extacting packages and improve the flow to save time.
