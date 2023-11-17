#Requires AutoHotkey v2.0
#SingleInstance

#r::
{
Send "{Click 292 974 Left}"
Sleep 100

Send "{Click 43 545 Left}"
Sleep 1000
Send "{Click 161 676 Left}"
Sleep 1000
;MsgBox "Select All"
;Sleep 1000
Send "^a"
Sleep 1000

;For high selection popup
Send "{Enter}"
Sleep 1000

Send "{Click 60 10 Left}"
Sleep 10
Loop 10
{
	Send "{Down}"
	Sleep 10
}

Send "{Right}"
Sleep 10
Send "{Down}"
Sleep 10
Send "{Enter}"
sleep 100

Send "{Enter}"
}