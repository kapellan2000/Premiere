@echo off
echo Premiere Pro plugin add
echo -----------------

set /p Input=Input path to Prism root: 
cd %~dp0
rmdir /s %Input%"\Plugins\Apps\Premiere"
mkdir %Input%"\Plugins\Apps\Premiere"
del %Input%"\ProjectFiles\EmptyScenes\EmptyScene Premiere 2021.prproj"

xcopy ".\Integration" %Input%"\Plugins\Apps\AfterEffects\Integration" /s /e /y /i /o
xcopy ".\Scripts" %Input%"\Plugins\Apps\AfterEffects\Scripts" /s /e /y /i /o
xcopy ".\UserInterfaces" %Input%"\Plugins\Apps\AfterEffects\UserInterfaces" /s /e /y /i /o

xcopy ".\Export.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Project Browser.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Save Extended.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Save Version.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o
xcopy ".\Settings.cmd" %Input%"\Plugins\Apps\AfterEffects" /s /e /y /i /o




xcopy /S /Q /Y /F ".\Integration\EmptyScene Premiere 2021.prproj" %Input%"\ProjectFiles\EmptyScenes\"

echo Complite
pause
