cd ../../
call ./backend/venv/Scripts/activate.bat
cd deploy_tools/
fab deploy --host=meinuser@bookmarks.christianw.de
PAUSE
