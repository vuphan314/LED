# rm -rf build/ dist/

# python3 pyinstaller/makespec.py led_engine.py -n led -F

python3 pyinstaller/pyinstaller.py led_man.spec

cd dist/ && ./led ../../examples/countingGame.led && cd ..
