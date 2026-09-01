# Requires Administrator Privileges
$TaskName = "AquariusServiceWatchdog"
$PythonPath = (Get-Command python).Source
$ScriptPath = "$PSScriptRoot\..\src\service_watchdog.py"

$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "$ScriptPath --once"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$Principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Force
Write-Host "Scheduled Task '$TaskName' registered successfully to run every 5 minutes." -ForegroundColor Green
