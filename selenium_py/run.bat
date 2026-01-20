@echo off
python -m selenium install >NUL 2>&1
python -u selenium_py\src\play_eplus_bot.py --config config\config.yaml --selectors config\selectors.json
echo run