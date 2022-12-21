echo off
CD /D "%~dp0"

start ..\..\..\Python39\pythonw.exe .\Scripts\Prism_Premiere_MenuTools.py SaveVersion
exit