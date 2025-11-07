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
        Comando para obtener los servicios no firmados en el sistema. Ahora puede exportar los resultados a CSV.
    .PARAMETER OutputPath
        Ruta del archivo CSV de salida. Por defecto: "$PWD\procesos_sin_firma_dd_MM_yyyy.csv"
    .PARAMETER DontSaveReport
        Si se especifica, no se guardará el CSV y sólo se devolverá la colección en memoria.
    #>
    [CmdletBinding()]
    param(
        [string]$OutputPath = "$PWD\procesos_sin_firma_$(Get-Date -Format dd_MM_yyyy).csv",
        [switch]$DontSaveReport
    )

    $processes = Get-Process
    $results = @()
    $detected = $false

    # Recorremos cada proceso y verificamos su firma digital
    foreach ($process in $processes) {
        $filePath = $process.Path
        if ($null -ne $filePath) {
            try {
                $signature = Get-AuthenticodeSignature -FilePath $filePath -ErrorAction Stop
                $status = $signature.Status
                $signer = if ($signature.SignerCertificate) { $signature.SignerCertificate.Subject } else { $null }
            }
            catch {
                # Si no se puede leer la firma, lo consideramos Unknown
                $status = 'Unknown'
                $signer = $null
            }

            if ($status -eq 'NotSigned' -or $status -eq 'Unknown') {
                Write-Host "Proceso no firmado detectado: $($process.ProcessName) (PID: $($process.Id)) - Ruta: $filePath"
                $detected = $true
                $results += [PSCustomObject]@{
                    ProcessName     = $process.ProcessName
                    PID             = $process.Id
                    Path            = $filePath
                    SignatureStatus = $status
                    Signer          = $signer
                }
            }
        }
    }

    # Exportar a CSV a menos que se pida omitirlo con el parámetro -DontSaveReport
    if (-not $DontSaveReport) {
        if ($results.Count -gt 0) {
            $results | Sort-Object ProcessName | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8
            Write-Host "Exportación completada. Archivo: $OutputPath"
        }
        else {
            Write-Output "No se detectaron procesos sin firma digital."
        }
    }

    return $results
}