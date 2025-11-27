@echo off
REM Multi-Agent Orchestrator - Quick Start Script for Windows
REM This script helps you quickly start and manage the multi-agent orchestrator service

setlocal enabledelayedexpansion

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Get command
set COMMAND=%1

if "%COMMAND%"=="" set COMMAND=help

REM Execute command
if "%COMMAND%"=="build" goto build
if "%COMMAND%"=="start" goto start
if "%COMMAND%"=="stop" goto stop
if "%COMMAND%"=="restart" goto restart
if "%COMMAND%"=="status" goto status
if "%COMMAND%"=="logs" goto logs
if "%COMMAND%"=="shell" goto shell
if "%COMMAND%"=="interactive" goto interactive
if "%COMMAND%"=="demo" goto demo
if "%COMMAND%"=="examples" goto examples
if "%COMMAND%"=="backup" goto backup
if "%COMMAND%"=="restore" goto restore
if "%COMMAND%"=="cleanup" goto cleanup
if "%COMMAND%"=="help" goto help
goto unknown

:build
echo ========================================
echo Building Multi-Agent Orchestrator Service
echo ========================================
docker-compose build multi_agent_orchestrator
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Service built successfully
) else (
    echo [ERROR] Build failed
    exit /b 1
)
goto end

:start
echo ========================================
echo Starting Multi-Agent Orchestrator Service
echo ========================================
docker-compose up -d ollama multi_agent_orchestrator
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Service started successfully
    echo [INFO] Waiting for services to be healthy...
    timeout /t 10 /nobreak >nul
    docker inspect --format="{{.State.Health.Status}}" multi_agent_orchestrator 2>nul | findstr "healthy" >nul
    if %ERRORLEVEL% EQU 0 (
        echo [SUCCESS] Service is healthy
    ) else (
        echo [WARNING] Service is starting... (may take up to 40 seconds)
    )
) else (
    echo [ERROR] Failed to start service
    exit /b 1
)
goto end

:stop
echo ========================================
echo Stopping Multi-Agent Orchestrator Service
echo ========================================
docker-compose stop multi_agent_orchestrator
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Service stopped successfully
) else (
    echo [ERROR] Failed to stop service
    exit /b 1
)
goto end

:restart
echo ========================================
echo Restarting Multi-Agent Orchestrator Service
echo ========================================
docker-compose stop multi_agent_orchestrator
timeout /t 2 /nobreak >nul
docker-compose up -d multi_agent_orchestrator
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Service restarted successfully
) else (
    echo [ERROR] Failed to restart service
    exit /b 1
)
goto end

:status
echo ========================================
echo Service Status
echo ========================================
docker ps | findstr multi_agent_orchestrator >nul
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Container is running
    docker inspect --format="{{.State.Health.Status}}" multi_agent_orchestrator 2>nul
    echo.
    echo Resource Usage:
    docker stats --no-stream multi_agent_orchestrator
) else (
    echo [ERROR] Container is not running
)
goto end

:logs
echo ========================================
echo Viewing Service Logs (Ctrl+C to exit)
echo ========================================
docker-compose logs -f multi_agent_orchestrator
goto end

:shell
echo ========================================
echo Entering Container Shell
echo ========================================
docker exec -it multi_agent_orchestrator bash
goto end

:interactive
echo ========================================
echo Running Interactive Mode
echo ========================================
docker exec -it multi_agent_orchestrator python agents/interactive.py
goto end

:demo
echo ========================================
echo Running Demo
echo ========================================
docker exec -it multi_agent_orchestrator python agents/demo.py
goto end

:examples
echo ========================================
echo Running Examples
echo ========================================
docker exec -it multi_agent_orchestrator python agents/main.py
goto end

:backup
echo ========================================
echo Backing Up Agent Memories and Logs
echo ========================================
set TIMESTAMP=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_DIR=backups\%TIMESTAMP%
mkdir "%BACKUP_DIR%" 2>nul

echo [INFO] Backing up agent memories...
docker run --rm -v orchestrator_data:/data -v "%CD%\%BACKUP_DIR%":/backup alpine tar czf /backup/agent_memories.tar.gz -C /data .
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Agent memories backed up to %BACKUP_DIR%\agent_memories.tar.gz
)

echo [INFO] Backing up logs...
docker run --rm -v orchestrator_logs:/data -v "%CD%\%BACKUP_DIR%":/backup alpine tar czf /backup/logs.tar.gz -C /data .
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Logs backed up to %BACKUP_DIR%\logs.tar.gz
)

echo [SUCCESS] Backup completed: %BACKUP_DIR%
goto end

:restore
if "%2"=="" (
    echo [ERROR] Please specify backup directory: orchestrator.bat restore backups\TIMESTAMP
    exit /b 1
)
set BACKUP_DIR=%2

if not exist "%BACKUP_DIR%" (
    echo [ERROR] Backup directory not found: %BACKUP_DIR%
    exit /b 1
)

echo ========================================
echo Restoring Data from %BACKUP_DIR%
echo ========================================

if exist "%BACKUP_DIR%\agent_memories.tar.gz" (
    echo [INFO] Restoring agent memories...
    docker run --rm -v orchestrator_data:/data -v "%CD%\%BACKUP_DIR%":/backup alpine sh -c "cd /data && tar xzf /backup/agent_memories.tar.gz"
    echo [SUCCESS] Agent memories restored
)

if exist "%BACKUP_DIR%\logs.tar.gz" (
    echo [INFO] Restoring logs...
    docker run --rm -v orchestrator_logs:/data -v "%CD%\%BACKUP_DIR%":/backup alpine sh -c "cd /data && tar xzf /backup/logs.tar.gz"
    echo [SUCCESS] Logs restored
)

echo [SUCCESS] Restore completed
goto end

:cleanup
echo ========================================
echo Cleaning Up
echo ========================================
echo [WARNING] This will remove the container and volumes. Are you sure? (Y/N)
set /p RESPONSE=
if /i "%RESPONSE%"=="Y" (
    docker-compose down multi_agent_orchestrator
    docker volume rm orchestrator_data orchestrator_logs 2>nul
    echo [SUCCESS] Cleanup completed
) else (
    echo [INFO] Cleanup cancelled
)
goto end

:help
echo Multi-Agent Orchestrator - Quick Start Script
echo.
echo Usage: orchestrator.bat [command]
echo.
echo Commands:
echo     build           Build the service
echo     start           Start the service
echo     stop            Stop the service
echo     restart         Restart the service
echo     status          Check service status
echo     logs            View service logs
echo     shell           Enter container shell
echo     interactive     Run interactive mode
echo     demo            Run demo
echo     examples        Run examples
echo     backup          Backup agent memories and logs
echo     restore [dir]   Restore from backup directory
echo     cleanup         Remove container and volumes
echo     help            Show this help message
echo.
echo Examples:
echo     orchestrator.bat build
echo     orchestrator.bat start
echo     orchestrator.bat logs
echo     orchestrator.bat interactive
echo     orchestrator.bat backup
echo     orchestrator.bat restore backups\20240115_120000
echo.
echo For more information, see services\multi_agent_orchestrator\README.md
goto end

:unknown
echo [ERROR] Unknown command: %COMMAND%
echo.
goto help

:end
endlocal
