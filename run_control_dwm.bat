::@echo off
::if "%1"=="h" goto begin
::start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:::begin

cmd /k "cd C:\Users\zhang\Desktop\dwm\control_dwm-main&&py Control_dwm.py"
::>control_dwm_log.txt"