Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\Users\musta\Desktop\app.bat" & Chr(34), 0
Set WinScriptHost = Nothing
