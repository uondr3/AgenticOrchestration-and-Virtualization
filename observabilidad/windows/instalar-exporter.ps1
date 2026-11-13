#Requires -RunAsAdministrator
<#
  Instala windows_exporter como servicio en una estación Windows.
  - Descarga el MSI oficial y verifica su SHA-256.
  - Activa los colectores del sistema, la tarjeta de video y los procesos elegidos.
  - Abre el puerto solo para direcciones de Tailscale.
  No requiere cerrar Revit ni 3ds Max.

  Uso, en PowerShell como administrador:
    .\instalar-exporter.ps1
#>
param(
  [string]$Version = "0.32.1",
  [string]$Sha256 = "8e1ade6a2fbcdeb4774c300b598667cd7888246be8fcc4b586d11b3680433981",
  [string]$PermitirDesde = "100.64.0.0/10",
  # Expresión regular sensible a mayúsculas, sin ".exe"
  [string]$Procesos = "(Revit|3dsmax|3dsmaxbatch|claude|rvt-mcp)",
  [string]$Colectores = "cpu,cpu_info,gpu,logical_disk,memory,net,os,physical_disk,process,system"
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$msi = "windows_exporter-$Version-amd64.msi"
$dir = Join-Path $env:TEMP "windows_exporter-$Version"
New-Item -ItemType Directory -Force $dir | Out-Null
$ruta = Join-Path $dir $msi

Write-Host "==> Descargando $msi"
Invoke-WebRequest "https://github.com/prometheus-community/windows_exporter/releases/download/v$Version/$msi" -OutFile $ruta
$hash = (Get-FileHash $ruta -Algorithm SHA256).Hash.ToLower()
if ($hash -ne $Sha256.ToLower()) { throw "La huella no coincide: $hash" }
Write-Host "    huella OK"

Write-Host "==> Instalando servicio"
$log = Join-Path $dir "instalacion.log"
$argumentos = @(
  "/i", "`"$ruta`"", "/qn", "/l*v", "`"$log`"",
  "ENABLED_COLLECTORS=$Colectores",
  "ADDLOCAL=FirewallException",
  "REMOTE_ADDR=$PermitirDesde",
  "EXTRA_FLAGS=`"--collector.process.include=$Procesos`""
)
$p = Start-Process msiexec.exe -ArgumentList $argumentos -Wait -PassThru
if ($p.ExitCode -ne 0) { throw "msiexec terminó con código $($p.ExitCode). Revisa $log" }

Write-Host "==> Verificación"
Start-Sleep 5
Get-Service windows_exporter | Format-Table Name, Status, StartType -AutoSize
$m = (Invoke-WebRequest "http://127.0.0.1:9182/metrics" -UseBasicParsing).Content -split "`n"
"    métricas totales:      " + ($m | Where-Object { $_ -notmatch "^#" }).Count
"    métricas de procesos:  " + ($m | Where-Object { $_ -match "^windows_process_" }).Count
"    métricas de GPU:       " + ($m | Where-Object { $_ -match "^windows_gpu_" }).Count
Get-NetFirewallRule -DisplayName "*windows_exporter*" -ErrorAction SilentlyContinue |
  Get-NetFirewallAddressFilter | Format-Table RemoteAddress -AutoSize
