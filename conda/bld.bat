robocopy %RECIPE_DIR%\.. . /E

set CONDA_ASSIMP_DIR=%LIBRARY_PREFIX%

"%PYTHON%" setup.py install --single-version-externally-managed --record=%TEMP%record.txt

if errorlevel 1 exit 1
