@echo off
REM ============================================================
REM  Publish the morform.app website to Cloudflare.
REM  Edit your site files, save, then double-click this file.
REM  It uploads everything to Cloudflare and the change goes
REM  live at https://morform.app within a few seconds.
REM ============================================================
cd /d "%~dp0"
echo.
echo   Publishing morform.app to Cloudflare...
echo.
call npx wrangler deploy
echo.
echo   Done. You can close this window.
pause >nul
