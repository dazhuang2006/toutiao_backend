param(
    [switch]$EnvOnly,
    [string]$MysqlServiceName = "MySQL80",
    [string]$RedisConfig = "D:\program\redis\redis.windows.conf",
    [string]$MilvusHome = "D:\program\docker_tool\Milvus",
    [string]$MilvusContainer = "milvus-standalone",
    [int]$BackendPort = 8010,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

function Test-PortOpen {
    param(
        [string]$HostName,
        [int]$Port
    )

    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $result = $client.BeginConnect($HostName, $Port, $null, $null)
        $ok = $result.AsyncWaitHandle.WaitOne(1000)
        if ($ok) {
            $client.EndConnect($result)
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
    finally {
        $client.Close()
    }
}

function Wait-PortOpen {
    param(
        [string]$Name,
        [string]$HostName,
        [int]$Port,
        [int]$TimeoutSeconds = 60
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (Test-PortOpen $HostName $Port) {
            Write-Host "[$Name] ready on $HostName`:$Port"
            return
        }
        Start-Sleep -Seconds 1
    }
    throw "[$Name] did not become ready on $HostName`:$Port within $TimeoutSeconds seconds"
}

function Start-MySql {
    if (Test-PortOpen "127.0.0.1" 3306) {
        Write-Host "[mysql] already listening on 3306"
        return
    }

    $svc = Get-Service -Name $MysqlServiceName -ErrorAction SilentlyContinue
    if (-not $svc) {
        $svc = Get-Service |
            Where-Object { $_.Name -like "*mysql*" -and $_.Name -notlike "*router*" } |
            Select-Object -First 1
    }

    if (-not $svc) {
        Write-Warning "[mysql] service not found; please start MySQL manually"
        return
    }

    if ($svc.Status -ne "Running") {
        try {
            Start-Service -Name $svc.Name
            Write-Host "[mysql] started service $($svc.Name)"
        }
        catch {
            Write-Warning "[mysql] failed to start service: $($_.Exception.Message)"
            return
        }
    }

    Wait-PortOpen "mysql" "127.0.0.1" 3306
}

function Start-Redis {
    if (Test-PortOpen "127.0.0.1" 6379) {
        Write-Host "[redis] already listening on 6379"
        return
    }

    $redisExe = (Get-Command redis-server -ErrorAction SilentlyContinue).Source
    if (-not $redisExe) {
        $redisExe = "D:\program\redis\redis-server.exe"
    }

    if (-not (Test-Path $redisExe)) {
        throw "[redis] executable not found: $redisExe"
    }

    $redisArgs = @()
    if (Test-Path $RedisConfig) {
        $redisArgs += $RedisConfig
    }

    $proc = Start-Process -FilePath $redisExe -ArgumentList $redisArgs `
        -WorkingDirectory (Split-Path $redisExe) -WindowStyle Hidden -PassThru
    Write-Host "[redis] started pid $($proc.Id)"
    Wait-PortOpen "redis" "127.0.0.1" 6379 15
}

function Test-DockerReady {
    docker version --format "{{.Server.Version}}" 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
}

function Start-Docker {
    if (Test-DockerReady) {
        Write-Host "[docker] engine ready"
        return
    }

    $svc = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -ne "Running") {
        try {
            Start-Service -Name $svc.Name
            Write-Host "[docker] started service $($svc.Name)"
        }
        catch {
            Write-Host "[docker] service needs admin or will start through Docker Desktop"
        }
    }

    $dockerDesktop = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if ((Test-Path $dockerDesktop) -and -not (Get-Process "Docker Desktop" -ErrorAction SilentlyContinue)) {
        Start-Process -FilePath $dockerDesktop -WindowStyle Hidden
        Write-Host "[docker] launching Docker Desktop"
    }

    $deadline = (Get-Date).AddSeconds(150)
    while ((Get-Date) -lt $deadline) {
        if (Test-DockerReady) {
            Write-Host "[docker] engine ready"
            return
        }
        Start-Sleep -Seconds 3
    }
    throw "[docker] engine did not become ready within 150 seconds"
}

function Start-Milvus {
    if (Test-PortOpen "127.0.0.1" 19530) {
        Write-Host "[milvus] already listening on 19530"
        return
    }

    if (-not (Test-DockerReady)) {
        throw "[milvus] docker engine is not ready"
    }

    $container = (docker ps -a --filter "name=$MilvusContainer" --format "{{.Names}}" | Select-Object -First 1)
    if ($container) {
        docker start $MilvusContainer | Out-Null
        Write-Host "[milvus] restarted existing container $MilvusContainer"
    }
    else {
        if (-not (Test-Path $MilvusHome)) {
            throw "[milvus] Milvus home not found: $MilvusHome"
        }

        Push-Location $MilvusHome
        try {
            docker run -d `
                --name $MilvusContainer `
                --security-opt seccomp:unconfined `
                -e ETCD_USE_EMBED=true `
                -e ETCD_DATA_DIR=/var/lib/milvus/etcd `
                -e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml `
                -e COMMON_STORAGETYPE=local `
                -e DEPLOY_MODE=STANDALONE `
                -v "${MilvusHome}\volumes\milvus:/var/lib/milvus" `
                -v "${MilvusHome}\embedEtcd.yaml:/milvus/configs/embedEtcd.yaml" `
                -v "${MilvusHome}\user.yaml:/milvus/configs/user.yaml" `
                -p 19530:19530 `
                -p 9091:9091 `
                -p 2379:2379 `
                milvusdb/milvus:v3.0.0 `
                milvus run standalone | Out-Null
            Write-Host "[milvus] created container $MilvusContainer"
        }
        finally {
            Pop-Location
        }
    }

    $deadline = (Get-Date).AddSeconds(180)
    while ((Get-Date) -lt $deadline) {
        $state = docker inspect -f "{{.State.Health.Status}}" $MilvusContainer 2>$null
        if ($state -eq "healthy") {
            Write-Host "[milvus] healthy"
            return
        }
        Start-Sleep -Seconds 5
    }
    throw "[milvus] container did not become healthy within 180 seconds"
}

function Start-Backend {
    if (Test-PortOpen "127.0.0.1" $BackendPort) {
        Write-Host "[backend] already listening on $BackendPort"
        return
    }

    $python = Join-Path $Root ".venv\Scripts\python.exe"
    if (-not (Test-Path $python)) {
        throw "[backend] virtualenv python not found: $python"
    }

    $logDir = Join-Path $Root "runtime_logs"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    $stdout = Join-Path $logDir "backend.log"
    $stderr = Join-Path $logDir "backend.err.log"

    $proc = Start-Process -FilePath $python `
        -ArgumentList @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", $BackendPort) `
        -WorkingDirectory $Root -WindowStyle Hidden `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    Write-Host "[backend] started pid $($proc.Id)"
    Wait-PortOpen "backend" "127.0.0.1" $BackendPort 60
}

function Start-Frontend {
    if (Test-PortOpen "127.0.0.1" $FrontendPort) {
        Write-Host "[frontend] already listening on $FrontendPort"
        return
    }

    $npm = (Get-Command npm.cmd -ErrorAction SilentlyContinue).Source
    if (-not $npm) {
        $npm = Join-Path $env:ProgramFiles "nodejs\npm.cmd"
    }
    if (-not (Test-Path $npm)) {
        throw "[frontend] npm not found"
    }

    $frontendDir = Join-Path $Root "frontend"
    if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
        throw "[frontend] node_modules not found; run npm install in frontend first"
    }

    $logDir = Join-Path $Root "runtime_logs"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    $stdout = Join-Path $logDir "frontend.log"
    $stderr = Join-Path $logDir "frontend.err.log"

    $env:VITE_API_URL = "http://127.0.0.1:$BackendPort"

    $proc = Start-Process -FilePath $npm `
        -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", $FrontendPort) `
        -WorkingDirectory $frontendDir -WindowStyle Hidden `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    Write-Host "[frontend] started pid $($proc.Id)"
    Wait-PortOpen "frontend" "127.0.0.1" $FrontendPort 60
}

Write-Host "Starting local services..."
Start-MySql
Start-Redis
Start-Docker
Start-Milvus

if (-not $EnvOnly) {
    Start-Backend
    Start-Frontend
}

Write-Host ""
Write-Host "Services summary:"
Write-Host "  MySQL    : 127.0.0.1:3306"
Write-Host "  Redis    : 127.0.0.1:6379"
Write-Host "  Milvus   : 127.0.0.1:19530"
if (-not $EnvOnly) {
    Write-Host "  Backend  : http://127.0.0.1:$BackendPort"
    Write-Host "  API docs : http://127.0.0.1:$BackendPort/docs"
    Write-Host "  Frontend : http://127.0.0.1:$FrontendPort"
}
Write-Host ""
Write-Host "Done."
