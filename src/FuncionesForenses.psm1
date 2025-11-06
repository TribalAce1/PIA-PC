# ============================================================================
# = Evidencia 7: Automatización de tareas forenses con PowerShell en Windows =
# ============================================================================


# 1. Extracción de eventos relevantes del Visor de eventos (registros de eventos)
function Get-SuspiciousEvents {
    <#
    .SYNOPSIS
        Comando para mostrar los eventos inusuales o sospechosos
    .DESCRIPTION
        Con este comando se extrae los eventos de Sistema, Aplicaciones y Seguridad y los filtra para encontrar todos los ventos sospechosos
    .PARAMETER MaxEvents
        Este parametro define el numero máximo de eventos ques se analizarán en cada log.
    .PARAMETER OutPath
        Especifica la ruta y el nombre del archivo CSV donde se guardarán los resultados
    #>
    param(
        [int]$MaxEvents = 2000,
        [string]$OutputPath = "$PWD\eventos_sospechosos_$(Get-Date -Format dd_MM_yyyy).csv",
        [switch]$DontSaveReport
    )

    # Logs a revisar
    $logs = "System", "Application", "Security"

    # IDs de eventos sospechosos comunes
    $idsSospechosos = 4625, 4672, 4648, 6008, 41, 7034, 7031, 1000, 1002

    # Palabras clave en los mensajes
    $keywords = "fail","denied","unauthorized","error","critical","malware","attack"

    foreach ($log in $logs) {
        try {
            Get-WinEvent -LogName $log -MaxEvents $MaxEvents |
            Where-Object {
                ($_.Id -in $idsSospechosos) -or
                ($_.LevelDisplayName -in "Error","Critical","Warning") -or
                ($keywords | ForEach-Object { $_match = $_; if ($_.Message -match $_match) { $true } })
            } |
            Select-Object @{Name="LogName";Expression={$log}},
                          TimeCreated,
                          Id,
                          LevelDisplayName,
                          @{Name="Message";Expression={$_.Message -replace "`r`n"," "}} |
                          ForEach-Object {
                                if (-not $DontSaveReport) {
                                    $_ | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8 -Append
                                }
                            Write-Output $_
                        }

        }
        catch {
            Write-Warning "No se pudo acceder al log $log (¿ejecutaste como Administrador?)."
        }
    }
    if (-not $DontSaveReport) {
        Write-Host "Exportación completada. Archivo: $OutputPath"
    }
}


# 2. Correlación de procesos activos con conexiones de red
#Get-InternetProcesses
function Get-InternetProcesses {
    <#
    .SYNOPSIS
        Comando para relacionar procesos que estan accediendo a internet
    .DESCRIPTION
        Este comando verifica las conexiones a internet y las relaciona a procesos que se estan ejecutando y genera un reporte en la ruta que se esta corriendo el comando
    .PARAMETER DontSaveReport
        Este parametro nos permite ejecutar el comando sin guardar el reporte
    #>
    [CmdletBinding()]
    param(
        [switch]$DontSaveReport
    )

    # Obtenemos todas las conexiones TCP establecidas
    $connections = Get-NetTCPConnection |
                   Where-Object State -eq 'Established'

    # Creamos un array de objetos con la informacion que necesaria
    $results = foreach ($conn in $connections) {
        try {
            $proc = Get-Process -Id $conn.OwningProcess -ErrorAction Stop
        }
        catch {
            continue
        }

        [PSCustomObject]@{
            ProcessName   = $proc.ProcessName
            PID           = $conn.OwningProcess
            LocalAddress  = $conn.LocalAddress
            LocalPort     = $conn.LocalPort
            RemoteAddress = $conn.RemoteAddress
            RemotePort    = $conn.RemotePort
            State         = $conn.State
        }
    }

    # Mostramos en pantalla los datos
    $results | Format-Table -AutoSize

    # Exportamos a CSV a menos que se pida omitirlo con el parámetro -DontSaveReport
    if (-not $DontSaveReport) {
        $results | Export-Csv -Path "$PWD\reporte_procesos_internet_$(Get-Date -Format dd_MM_yyyy).csv" -NoTypeInformation
    }
}


#Get-UnsignedProcesses
function Get-UnsignedProcesses {
    <#
    .SYNOPSIS
        Comando para obtener los servicios no firmados en el sistema
    .DESCRIPTION
        Comando para obtener los servicios no firmados en el sistema
    #>
    $processes = Get-Process
    $detected = $null

    # Recorremos cada proceso y verificamos su firma digital
    foreach ($process in $processes) {
        $filePath = $process.Path
        if ($null -ne $filePath) { 
            $signature = Get-AuthenticodeSignature -FilePath "$filePath"
            if ($signature.Status -eq 'NotSigned' -or $signature.Status -eq 'Unknown') {
                Write-Host "Proceso no firmado detectado: $($process.ProcessName) (PID: $($process.Id)) - Ruta: $filePath"
                # Si se detecta al menos un proceso sin firma cambiamos el valor de $detected de null a 1
                $detected = 1
            }
        }
    }

    # Si no se detectó ningún proceso sin firma, mostramos un mensaje indicándolo
    if ($null -eq $detected) {
        Write-Output "No se detectaron procesos sin firma digital."
    }
}


# 3. Investigación de direcciones IP remotas mediante AbuseIPDB
function Get-SuspiciousInternetProcesses {
    <#
    .SYNOPSIS
        Comando que verifica las conexiones a internet y ivestiga si son confiables con el api de AbuseIPDB
    .DESCRIPTION
        Comando que verifica las conexiones a internet y ivestiga si son confiables con el api de AbuseIPDB y guarda un reporte
    .PARAMETER DontSaveReport
        Este parametro nos permite ejecutar el comando sin guardar el reporte
    .PARAMETER Threshold
        Este parametro nos permite ajustar la sensibilidad de la deteccion de AbuseIPDB [int] 0-100 
    #>
    [CmdletBinding()]
    param(
        [int] $Threshold = 10,

        [switch]$DontSaveReport
    )


    # Inicializar la lista de resultados
    $results = @()

    # Obtener conexiones TCP establecidas
    $TCPConnections = Get-NetTCPConnection | Where-Object State -eq "Established"
    $Processes = Get-Process

    foreach ($connection in $TCPConnections) {
        $ip = $connection.RemoteAddress

        try {
            # Llamada a AbuseIPDB
            $response = Invoke-RestMethod -Method Get `
                -Uri "https://api.abuseipdb.com/api/v2/check?ipAddress=$ip" `
                -Headers @{
                    "Key"    = "yourapikey"
                    "Accept" = "application/json"
                }

            $score = $response.data.abuseConfidenceScore

            # Agregar sólo si supera el umbral
            if ($score -ge $Threshold) {
                $proc = $Processes | Where-Object Id -eq $connection.OwningProcess
                $results += [PSCustomObject]@{
                    Timestamp          = (Get-Date).ToString("s")
                    ProcessName        = $proc.ProcessName
                    PID                = $proc.Id
                    RemoteAddress      = $ip
                    AbuseConfidencePct = $score
                    TotalReports       = $response.data.totalReports
                }
            }
        }
        catch {
            Write-Warning "Error consultando AbuseIPDB"
        }
    }

    # Exportar todos los resultados a CSV
    if (-not $DontSaveReport){
        if ($results.Count -gt 0) {
            $results | Sort-Object AbuseConfidencePct -Descending |
                Export-Csv -Path "$PWD\processos_sospechosos_abuseipdb_$(Get-Date -Format dd_MM_yyyy).csv" -NoTypeInformation -Encoding UTF8
        }
        else {
            Write-Output "No se encontraron IPs con puntaje de abuso mayor a $Threshold."
    }
    }

    return $results
}

function Get-FullForensicAnalysis {
    [CmdletBinding()]
    param(
        [string]$OutputPath = ".\Full_Forensic_Report_{0}.csv" -f (Get-Date -Format "dd_MM_yyyy_HH_mm"),
        [switch]$DontSaveReport
    )

    Write-Host "=== Iniciando análisis forense completo ===" -ForegroundColor Cyan

    # 1. Obtener eventos sospechosos
    Write-Host "[1/4] Extrayendo eventos sospechosos del Visor de eventos..." -ForegroundColor Yellow
    $eventos = Get-SuspiciousEvents -DontSaveReport

    # 2. Obtener procesos con conexiones de red
    Write-Host "[2/4] Correlacionando procesos activos con conexiones de red..." -ForegroundColor Yellow
    $internetProcs = Get-InternetProcesses -DontSaveReport

    # 3. Obtener procesos con firmas no válidas
    Write-Host "[3/4] Detectando procesos sin firma digital..." -ForegroundColor Yellow
    $unsignedProcs = Get-UnsignedProcesses

    # 4. Procesos con IPs sospechosas (AbuseIPDB)
    Write-Host "[4/4] Consultando IPs sospechosas en AbuseIPDB..." -ForegroundColor Yellow
    $suspiciousIPs = Get-SuspiciousInternetProcesses -Threshold 10 -DontSaveReport

    # --- Correlación ---
    Write-Host "Correlacionando resultados..." -ForegroundColor Green

    # Convertir a tablas para correlación por nombre de proceso o PID
    $internetProcsTable = $internetProcs | Select-Object ProcessName, Id, RemoteAddress
    $unsignedProcsTable = $unsignedProcs | Select-Object ProcessName, Id
    $suspiciousIPsTable = $suspiciousIPs | Select-Object ProcessName, Id, RemoteAddress

    # Unir datos por coincidencia de PID o nombre
    $correlacion = @()

    foreach ($proc in $internetProcsTable) {
        $matchUnsigned = $unsignedProcsTable | Where-Object { $_.Id -eq $proc.Id }
        $matchSuspiciousIP = $suspiciousIPsTable | Where-Object { $_.Id -eq $proc.Id }

        if ($matchUnsigned -or $matchSuspiciousIP) {
            $correlacion += [PSCustomObject]@{
                ProcessName   = $proc.ProcessName
                PID           = $proc.Id
                RemoteAddress = $proc.RemoteAddress
                Unsigned      = if ($matchUnsigned) { $true } else { $false }
                SuspiciousIP  = if ($matchSuspiciousIP) { $true } else { $false }
            }
        }
    }

    # --- Generar reporte ---
    if (-not $DontSaveReport) {
        $correlacion | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8
        Write-Host "Reporte generado en: $OutputPath" -ForegroundColor Cyan
    }

    Write-Host "=== Análisis forense completo finalizado ===" -ForegroundColor Cyan
    return $correlacion
}