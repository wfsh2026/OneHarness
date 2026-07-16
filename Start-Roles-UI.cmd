@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHON_EXE="
set "PYTHON_ARGS="

if not "%THARNESS_PYTHON%"=="" goto check_env_python
goto try_py_launcher

:check_env_python
if exist "%THARNESS_PYTHON%" goto use_env_python
echo 警告：THARNESS_PYTHON 指向的文件不存在：%THARNESS_PYTHON%
goto try_py_launcher

:use_env_python
set "PYTHON_EXE=%THARNESS_PYTHON%"
goto launch

:try_py_launcher
where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 -c "import sys" >nul 2>nul
if errorlevel 1 goto try_python
set "PYTHON_EXE=py"
set "PYTHON_ARGS=-3"
goto launch

:try_python
where python >nul 2>nul
if errorlevel 1 goto try_python3
python -c "import sys" >nul 2>nul
if errorlevel 1 goto try_python3
set "PYTHON_EXE=python"
goto launch

:try_python3
where python3 >nul 2>nul
if errorlevel 1 goto try_codex_python
python3 -c "import sys" >nul 2>nul
if errorlevel 1 goto try_codex_python
set "PYTHON_EXE=python3"
goto launch

:try_codex_python
set "PYTHON_EXE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%PYTHON_EXE%" goto launch
set "PYTHON_EXE="
goto try_python314

:try_python314
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
if exist "%PYTHON_EXE%" goto launch
goto try_python313

:try_python313
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if exist "%PYTHON_EXE%" goto launch
goto try_python312

:try_python312
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PYTHON_EXE%" goto launch
goto try_python311

:try_python311
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if exist "%PYTHON_EXE%" goto launch
goto try_python310

:try_python310
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%PYTHON_EXE%" goto launch
goto python_not_found

:python_not_found
echo.
echo 错误：未找到可用的 Python 3，角色浏览器无法启动。
echo 可安装 Python 3 并加入 PATH，或设置 THARNESS_PYTHON 为 python.exe 的完整路径。
echo 示例：set THARNESS_PYTHON=C:\Path\To\python.exe
echo.
pause
exit /b 1

:launch
echo 正在启动 Tharness 角色浏览器...
echo 使用解释器：%PYTHON_EXE% %PYTHON_ARGS%
echo 浏览器未自动打开时，请使用窗口中显示的本地地址。
echo.
call "%PYTHON_EXE%" %PYTHON_ARGS% "%~dp0tools\tharness.py" roles-ui %*
set "EXIT_CODE=%ERRORLEVEL%"
if "%EXIT_CODE%"=="0" goto launcher_done
echo.
echo 角色浏览器启动失败，Python 退出码：%EXIT_CODE%
echo 请检查上方错误；也可设置 THARNESS_PYTHON 指定可用解释器。
pause

:launcher_done
exit /b %EXIT_CODE%
