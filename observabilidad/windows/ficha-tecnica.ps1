# Lee la ficha técnica de la estación (solo lectura). Uso: powershell -File ficha-tecnica.ps1
$o=[ordered]@{}
$c=Get-CimInstance Win32_Processor; $o.cpu="$($c.Name.Trim()) | $($c.NumberOfCores) núcleos / $($c.NumberOfLogicalProcessors) hilos"
$b=Get-CimInstance Win32_BaseBoard; $o.placa="$($b.Manufacturer) $($b.Product)"
$o.slots=(Get-CimInstance Win32_PhysicalMemoryArray).MemoryDevices
$o.ram=@(Get-CimInstance Win32_PhysicalMemory | ForEach-Object { "$($_.DeviceLocator)|$([math]::Round($_.Capacity/1GB))|$($_.ConfiguredClockSpeed)|$($_.Speed)|$($_.Manufacturer)|$($_.PartNumber.Trim())" })
$o.gpu=@(Get-CimInstance Win32_VideoController | ForEach-Object { "$($_.Name)|$($_.DriverVersion)" })
$o.discos=@(Get-PhysicalDisk | ForEach-Object { "$($_.FriendlyName)|$([math]::Round($_.Size/1GB))|$($_.MediaType)|$($_.BusType)" })
$v=Get-CimInstance Win32_OperatingSystem; $o.so="$($v.Caption) $($v.DisplayVersion) build $($v.BuildNumber)"
$o.bios=(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion
"SPECS_JSON=" + ($o | ConvertTo-Json -Compress)
