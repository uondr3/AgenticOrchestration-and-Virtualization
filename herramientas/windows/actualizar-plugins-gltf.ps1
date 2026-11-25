# Actualiza el exportador y el importador glTF de Khronos en 3ds Max 2021.
# Uso, desde PowerShell con permiso de administrador y con 3ds Max cerrado:
#   .\actualizar-plugins-gltf.ps1 -Origen "<carpeta con los dos archivos nuevos>"
# Comprueba la huella SHA-256 de los archivos nuevos, respalda los actuales y verifica la copia.
# El resultado queda en C:\ProgramData\UONDR-obs\plugins-gltf.log
param(
    [Parameter(Mandatory = $true)][string]$Origen,
    [string]$Plugins = "C:\Program Files\Autodesk\3ds Max 2021\Plugins"
)
$ErrorActionPreference = "Stop"
$esperado = @{
    "KHRglTFExporter_2021.dle" = "BB696AF829F812CA6E5F1FD7F5AE95A8A7A371EF644EFC28139FC88BACE77C5C"
    "KHRglTFImporter_2021.dli" = "3568998207541D8436D41387289E324571A12BF5418663836D00A0A7031BF068"
}
$dirLog = "C:\ProgramData\UONDR-obs"
New-Item -ItemType Directory -Force $dirLog | Out-Null
$log = Join-Path $dirLog "plugins-gltf.log"
function Anotar([string]$t) {
    $linea = (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " " + $t
    Add-Content -Path $log -Value $linea -Encoding UTF8
    Write-Output $linea
}
try {
    Anotar "INICIO origen=$Origen"
    if (Get-Process -Name "3dsmax", "3dsmaxbatch" -ErrorAction SilentlyContinue) {
        throw "3ds Max esta abierto. Cierralo y vuelve a correr."
    }
    if (-not (Test-Path $Plugins)) { throw "No existe la carpeta de plugins: $Plugins" }
    foreach ($nombre in $esperado.Keys) {
        $nuevo = Join-Path $Origen $nombre
        if (-not (Test-Path $nuevo)) { throw "Falta el archivo nuevo: $nombre" }
        $h = (Get-FileHash $nuevo -Algorithm SHA256).Hash
        if ($h -ne $esperado[$nombre]) { throw "Huella incorrecta en el archivo nuevo: $nombre" }
    }
    $marca = Get-Date -Format "yyyyMMdd"
    foreach ($nombre in $esperado.Keys) {
        $destino = Join-Path $Plugins $nombre
        if (Test-Path $destino) {
            $actual = (Get-FileHash $destino -Algorithm SHA256).Hash
            if ($actual -eq $esperado[$nombre]) { Anotar "YA_AL_DIA $nombre"; continue }
            $respaldo = "$destino.before-$marca-update"
            if (-not (Test-Path $respaldo)) { Copy-Item $destino $respaldo }
            Anotar "RESPALDO $nombre anterior=$actual"
        }
        Copy-Item (Join-Path $Origen $nombre) $destino -Force
        $final = (Get-FileHash $destino -Algorithm SHA256).Hash
        if ($final -ne $esperado[$nombre]) { throw "La copia no quedo con la huella esperada: $nombre" }
        Anotar "ACTUALIZADO $nombre"
    }
    Anotar "RESULTADO OK"
}
catch {
    Anotar ("RESULTADO ERROR " + $_.Exception.Message)
    exit 1
}
