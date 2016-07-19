Tools to make Linux parser easier to use.
=========================================
Feature:
--------
1. Find vmlinux and dump log in folder, then set the correct path.

2. If vmlinux or dump log is in archive, such as zip format, it will be extracted automatically. Then set the path.

Usage:
------
1. Unzip this tool into ramdump tool. Such as D:\ramdump8976\dumpLogTool\checkdump.bat

2. Modify ini file to your real path if needed.

3. Open cmd.exe and run:<br/>
D:\ramdump8976\dumpLogTool\checkdump.bat vmlinux_path log_path [platform]<br/>
platform is optional. Such as 8909, 8976, 8939. This will map to dump8909.bat, dump8976.bat, dump8939.bat.

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
