Completes the process of the dwm.exe if consumes a lot of memory

ModeleControlProcess.py与Control_dwm.py中可以修改程序名称、限制大小、检测时间间隔

当前参数：每隔600s检测一次dwm.exe内存占用情况，超过1024MB后关闭程序
	      程序运行情况log输出到“日期.log”文件中，可以手动删除


ModeleControlProcess.py and Control_dwm.py can modify the program name, limit size, and detection time interval

Current parameters: Check the memory usage of dwm.exe every 600s, and close the program when it exceeds 1024MB
		The program operation log is output to the "date.log" file, which can be deleted manually
