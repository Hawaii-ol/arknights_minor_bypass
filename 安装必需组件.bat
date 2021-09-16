@echo off
where pip3>nul 2>nul
if %errorlevel% NEQ 0 (
  echo 没有找到pip3，请先安装python3！
  pause
  exit
)
::pip3 install --no-index --find-links=site-packages\ -r requirements.txt
pip3 install -r requirements.txt
if %errorlevel%==0 (
  echo 安装完成！
) else (
  echo 安装失败！
)
pause