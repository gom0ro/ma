@echo off
set BACKUP_DIR=backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

set TIMESTAMP=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2%_%TIME:~0,2%-%TIME:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo Creating backup of CanteenPay database...
copy backend\sql_app.db %BACKUP_DIR%\sql_app_backup_%TIMESTAMP%.db

echo.
echo Backup created in: %BACKUP_DIR%
pause
