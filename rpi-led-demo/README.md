# Raspberry Pi Demo

## Requirements
- Raspberry Pi 3 B (Other versions will also work but pin configuration might differ)
- 5 x male-female jumper wires
- 4 x 33 Ohm resistor (330 Ohm recommended by other guides)
- 4 x LED
- Bread Board

## Useful Links
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/#)

## Circuit
- [Turning on an LED with your Raspberry Pi's GPIO Pins [Guide]](https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)

## LED Watcher
```
pipenv shell
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt # Optional

python3 ./led-watcher.py
```
