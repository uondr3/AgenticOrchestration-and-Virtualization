#Requires -RunAsAdministrator
<#
  Instala la lectura de temperatura del procesador en una estación Windows.

  - PawnIO 2.2.0: controlador firmado que permite leer los sensores del procesador.
    Sustituye al antiguo WinRing0, que Windows Defender bloquea.
  - OhmGraphite 0.38.0: servicio que lee los sensores con LibreHardwareMonitor
    y los publica para Prometheus en el puerto 4445.
  - Abre el puerto 4445 solo para direcciones de Tailscale.

  Descargas oficiales verificadas por SHA-256. No requiere cerrar Revit ni 3ds Max.

  Uso, en PowerShell como administrador:
    .\instalar-temperatura.ps1
  Desinstalar:
    & "C:\Program Files\OhmGraphite\OhmGraphite.exe" stop; & "C:\Program Files\OhmGraphite\OhmGraphite.exe" uninstall
    PawnIO: Configuración → Aplicaciones → PawnIO → Desinstalar
#>
param(
  [string]$PawnIOVersion = "2.2.0",
  [string]$PawnIOSha256 = "1f519a22e47187f70a1379a48ca604981c4fcf694f4e65b734aaa74a9fba3032",
  [string]$OhmVersion = "0.38.0",
  [string]$OhmSha256 = "35dc1fea76f3f2f766ea0d416a1ac01ce61e3e6c239e13aad97b29d7ec9de418",
  [int]$Puerto = 4445,
  [string]$PermitirDesde = "100.64.0.0/10",
  [string]$Destino = "C:\Program Files\OhmGraphite"
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$tmp = Join-Path $env:TEMP "uondr-temperatura"
New-Item -ItemType Directory -Force $tmp | Out-Null

function Descargar($url, $archivo, $sha) {
  $ruta = Join-Path $tmp $archivo
  Invoke-WebRequest $url -OutFile $ruta -UseBasicParsing
  $h = (Get-FileHash $ruta -Algorithm SHA256).Hash.ToLower()
  if ($h -ne $sha.ToLower()) { throw "La huella de $archivo no coincide: $h" }
  Write-Host "    $archivo huella OK"
  return $ruta
}

Write-Host "==> PawnIO $PawnIOVersion"
$pawn = Descargar "https://github.com/namazso/PawnIO.Setup/releases/download/$PawnIOVersion/PawnIO_setup.exe" "PawnIO_setup.exe" $PawnIOSha256
$p = Start-Process $pawn -ArgumentList "-install", "-silent" -Wait -PassThru
if ($p.ExitCode -notin 0, 3010) { throw "PawnIO terminó con código $($p.ExitCode)" }
Write-Host "    instalado (código $($p.ExitCode))"

Write-Host "==> OhmGraphite $OhmVersion"
$zip = Descargar "https://github.com/nickbabcock/OhmGraphite/releases/download/v$OhmVersion/OhmGraphite-$OhmVersion.zip" "OhmGraphite-$OhmVersion.zip" $OhmSha256
$exe = Join-Path $Destino "OhmGraphite.exe"
if (Test-Path $exe) { & $exe stop 2>$null | Out-Null; Start-Sleep 3 }
New-Item -ItemType Directory -Force $Destino | Out-Null
Expand-Archive $zip $Destino -Force

$config = @"
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
  <appSettings>
    <add key="type" value="prometheus" />
    <add key="prometheus_port" value="$Puerto" />
    <add key="prometheus_host" value="*" />
    <add key="prometheus_path" value="metrics/" />
  </appSettings>
</configuration>
"@
[IO.File]::WriteAllText((Join-Path $Destino "OhmGraphite.exe.config"), $config, (New-Object Text.UTF8Encoding $false))

if (-not (Get-Service OhmGraphite -ErrorAction SilentlyContinue)) { & $exe install | Out-Null }
& $exe start | Out-Null

Write-Host "==> Firewall"
Get-NetFirewallRule -DisplayName "UONDR OhmGraphite" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
New-NetFirewallRule -DisplayName "UONDR OhmGraphite" -Direction Inbound -Protocol TCP -LocalPort $Puerto `
  -RemoteAddress $PermitirDesde -Action Allow -Profile Any | Out-Null

Write-Host "==> Verificación"
Start-Sleep 8
Get-Service OhmGraphite | Format-Table Name, Status, StartType -AutoSize
$m = (Invoke-WebRequest "http://127.0.0.1:$Puerto/metrics" -UseBasicParsing).Content -split "`n"
"    métricas totales:       " + ($m | Where-Object { $_ -notmatch "^#" }).Count
"    sensores de temperatura del procesador:"
$m | Where-Object { $_ -match "^ohm_cpu_celsius" } | Select-Object -First 8 | ForEach-Object { "      $_" }
Get-NetFirewallRule -DisplayName "UONDR OhmGraphite" | Get-NetFirewallAddressFilter | Format-Table RemoteAddress -AutoSize
