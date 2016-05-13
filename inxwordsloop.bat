
:loop

@date/t && time/t
@inxwords.py -nw --loop -d 1 -y M:\bin\data\inxwords.yaml
@date/t && time/t

@sleep 60 REM 1 mins (sleep.exe not on all WinXP)

goto loop
