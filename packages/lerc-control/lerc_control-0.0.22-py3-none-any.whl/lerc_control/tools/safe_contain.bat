@echo off

set seconds=%1

:: Get the PathName to the lerc service so this can work no-matter where lerc is installed.
SETLOCAL ENABLEDELAYEDEXPANSION
SET count=1
FOR /F "tokens=* USEBACKQ" %%F IN (`wmic service lerc get PathName`) DO (
  SET var!count!=%%F
  SET /a count=!count!+1
)
set lercpath=%var2%
echo Found lercpath: %lercpath%

:: A small delay to allow the client to check back in with the server before the firewall resets it's connection
:: ~2 second delay
PING localhost -n 2 >NUL

:CONTAIN
netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound
netsh advfirewall firewall add rule name="LERC" dir=out action=allow program=%lercpath% enable=yes
:: Default lerc service path for Integral Defense
::netsh advfirewall firewall add rule name="DefaultLERC" dir=out action=allow program="C:\Program Files (x86)\Integral Defense\Live Endpoint Response Client\lerc.exe" enable=yes
netsh advfirewall firewall add rule name="CBlack" dir=out action=allow program="C:\Windows\CarbonBlack\cb.exe" enable=yes
netsh advfirewall firewall add rule name="WinLogBeat" dir=out action=allow program="C:\Program Files\Winlogbeat\winlogbeat.exe" enable=yes
netsh advfirewall set allprofiles state on
netsh advfirewall show allprofiles

ENDLOCAL
:CHECK
:: delay by ~seconds argument
PING localhost -n %seconds% >NUL
GOTO Free

:FREE
ECHO RESETTING FIREWALL
netsh advfirewall reset
