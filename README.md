# ds4_driver

DualShock 4 driver for ROS2 dashing.

## Features

- Get information such as IMU, battery, and touchpad from your DualShock 4.
- Use feedback such as rumble, LED color, and LED flash via ROS topics.
- Connect to your controller via Bluetooth.

## Usage

This driver depends on `ds4drv`. Some features of this driver depend on pull
requests have not yet been merged upstream. Until they are merged, use
[`naoki-mizuno/ds4drv`](https://github.com/naoki-mizuno/ds4drv/tree/devel)
(`devel` branch).

```console
$ git clone https://github.com/naoki-mizuno/ds4drv --branch devel
$ cd ds4drv
$ python2 setup.py install --prefix ~/.local
$ sudo cp 50-ds4drv.rules /etc/udev/rules.d/
$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
```

Note: If you want to prevent the touchpad from being recognized as an input
device, add the following to the udev rules and run the `udevadm` commands
(you will still be able to use the touchpad from this driver):

```
SUBSYSTEM=="input", ATTRS{name}=="*Wireless Controller Touchpad", RUN+="/bin/rm %E{DEVNAME}", ENV{ID_INPUT_JOYSTICK}=""
```

Compile and source this package just like any other ROS package. To run,

```console
$ ros2 run ds4_driver ds4_driver_node.py
```

## Topics

### Published

- `/status` (`ds4_driver/Status`): current state of the device.

### Subscribed

- `/set_feedback` (`ds4_driver/Feedback`): feedback for the device such as
  LED color, rumble, and LED flash.

Note: To disable flash, send message with `set_led_flash: true` and
`led_flash_off: 0`.

## License

MIT

## Author

Original: Naoki Mizuno (naoki.mizuno.256@gmail.com)
Modify: sss22213 (n0404.n0404@gmail.com)


