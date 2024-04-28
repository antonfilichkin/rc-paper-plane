# 🛩️ RC Paper Plane 🛩️

RC paper plane project

### Table Of Contents

<ol>
  <li>
    <a href="#hardware-list">Hardware list</a>
    <ul><li><a href="#paper">Paper</a></li></ul>
    <ul><li><a href="#esp32-c3">ESP32 C3</a></li></ul>
    <ul><li><a href="#joystick">Joystick</a></li></ul>
  </li>
  <li>
    <a href="#required-software-and-tools">Required software and tools</a>
  </li>
  <li>
    <a href="#initial-configuration">Initial configuration</a></li>
</ol>

## Hardware list

### Paper

TODO

### ESP32 C3

TODO

### Joystick

TODO

## Required software and tools

1. [Esptool.py](https://docs.espressif.com/projects/esptool/en/latest/esp32/)
   or [Online ESP Tool](https://espressif.github.io/esptool-js/)

```sh
pip install esptool
```

## Initial configuration

1. Download latest [firmware](https://micropython.org/download/ESP32_GENERIC_C3/).
2. Erase flash:

```sh
esptool.py --chip esp32c3 --port {YOUR_BOARD_COM_PORT} erase_flash
```

4. Flash MicroPython firmware starting at address 0x0:

```sh
esptool.py --chip esp32c3 --port {YOUR_BOARD_COM_PORT} --baud 460800 write_flash -z 0x0 {FIRMWARE_FILE}
```

```sh
esptool.py --chip esp32c3 --port {YOUR_BOARD_COM_PORT} --no-stub --baud 460800 write_flash -z 0x0 {FIRMWARE_FILE}
```

To force bootloader mode for esp32c3 connect PIN9 to GND
see: [Boot mode selection](https://docs.espressif.com/projects/esptool/en/latest/esp32c3/advanced-topics/boot-mode-selection.html).

2. PyCharm
   File > Settings > Languages & Frameworks - MicroPython:

- ☑ **MicroPython**
- Device type **ESP8266**
- Device path **COM PORT**

<p align="right">(<a href="#table-of-contents">back to contents</a>)</p>