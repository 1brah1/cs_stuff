@echo off
REM Script to generate visualizations and prepare for commit
echo ============================================================
echo Stock Portfolio Visualization Generator
echo ============================================================
echo.

REM Activate conda base environment
echo Activating conda environment...
call %USERPROFILE%\miniconda3\Scripts\activate.bat base

REM Navigate to script directory
cd /d "%~dp0"

REM Run the visualization script
echo.
echo Generating visualizations...
python main.py

REM Check if visualizations were created
if exist "visualizations\*.png" (
    echo.
    echo ============================================================
    echo SUCCESS! Visualizations generated.
    echo ============================================================
    echo.
    echo Generated files:
    dir /b visualizations\*.png
    echo.
    echo Next steps:
    echo 1. Review the images in the visualizations folder
    echo 2. Commit them to git:
    echo    git add stock_analysis_portfolio/visualizations/*.png
    echo    git commit -m "Add stock portfolio visualizations"
    echo    git push
) else (
    echo.
    echo ERROR: No visualization files were generated.
    echo Please check the error messages above.
)

pause



