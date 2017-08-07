# python3 pyinstaller/makespec.py led_engine.py -n led -F
python3 pyinstaller/pyinstaller.py led_man.spec --distpath=.
rm -rf build/ __pycache__/
