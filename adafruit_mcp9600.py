# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_mcp9600`
================================================================================

CircuitPython driver for the MCP9600 thermocouple I2C amplifier.


* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit MCP9600 >url>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from micropython import const
import adafruit_bus_device.i2c_device as i2cdevice
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits, ROBits
from adafruit_register.i2c_bit import RWBit, ROBit

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP9600.git"


class MCP9600:
    # Thermocouple Type
    TYPE_K = const(0x0)
    TYPE_J = const(0x1)
    TYPE_T = const(0x2)
    TYPE_N = const(0x3)
    TYPE_S = const(0x4)
    TYPE_E = const(0x5)
    TYPE_B = const(0x6)
    TYPE_R = const(0x7)

    # Filter Coefficient
    FC_0 = const(0x0)
    FC_1 = const(0x1)
    FC_2 = const(0x2)
    FC_3 = const(0x3)
    FC_4 = const(0x4)
    FC_5 = const(0x5)
    FC_6 = const(0x6)
    FC_7 = const(0x7)

    # ADC Measurement Resolution
    ADC_18 = const(0x0)
    ADC_16 = const(0x1)
    ADC_14 = const(0x2)
    ADC_12 = const(0x3)

    # Burst Mode Temperature Samples
    BURST_1 = const(0x0)
    BURST_2 = const(0x1)
    BURST_4 = const(0x2)
    BURST_8 = const(0x3)
    BURST_16 = const(0x4)
    BURST_32 = const(0x5)
    BURST_64 = const(0x6)
    BURST_128 = const(0x7)

    # Shutdown Modes
    NORMAL = const(0x0)
    SHUTDOWN = const(0x1)
    BURST = const(0x2)

    # Hot-Junction Temperature (T sub H) "thermocouple temperature register"- 0x0
    _hot_junction_temperature = ROUnaryStruct(0x0, ">H")
    # Junctions Temperature Delta (T sub delta) "THERMOCOUPLE JUNCTIONS DELTA TEMPERATURE REGISTER" - 0x1
    _junctions_temperature_delta = ROUnaryStruct(0x1, ">H")
    # Cold-Junction Temperature (T sub C) "COLD-JUNCTION/AMBIENT TEMPERATURE REGISTER" - 0x2
    _cold_junction_temperature = ROUnaryStruct(0x2, ">H")
    # Raw data ADC - 0x3
    raw_adc = ROUnaryStruct(0x3, ">H")
    # STATUS - 0x4
    burst_complete = RWBit(0x4, 7, register_width=1)
    temperature_update = RWBit(0x4, 6, register_width=1)
    input_range = ROBit(0x4, 4, register_width=1)
    alert_4 = ROBit(0x4, 3, register_width=1)
    alert_3 = ROBit(0x4, 2, register_width=1)
    alert_2 = ROBit(0x4, 1, register_width=1)
    alert_1 = ROBit(0x4, 0, register_width=1)
    # Thermocouple Sensor Configuration - 0x5
    thermocouple_type = RWBits(3, 0x5, 4, register_width=1)
    filter_coefficient = RWBits(3, 0x5, 0, register_width=1)
    # Device Configuration - 0x6
    cold_junction_resolution = RWBit(0x6, 7, register_width=1)
    adc_resolution = RWBits(2, 0x6, 5, register_width=1)
    burst_mode = RWBits(3, 0x6, 2, register_width=1)
    shutdown_mode = RWBits(2, 0x6, 0, register_width=1)
    # Alert 1 Configuration - 0x8
    alert_1_int_clear = RWBit(0x8, 7, register_width=1)
    alert_1_temp_monitor = RWBit(0x8, 4, register_width=1)
    alert_1_temp_direction = RWBit(0x8, 3, register_width=1)
    alert_1_state = RWBit(0x8, 2, register_width=1)
    alert_1_mode = RWBit(0x8, 1, register_width=1)
    alert_1_enable = RWBit(0x8, 0, register_width=1)
    # Alert 2 Configuration - 0x9
    alert_2_int_clear = RWBit(0x9, 7, register_width=1)
    alert_2_temp_monitor = RWBit(0x9, 4, register_width=1)
    alert_2_temp_direction = RWBit(0x9, 3, register_width=1)
    alert_2_state = RWBit(0x9, 2, register_width=1)
    alert_2_mode = RWBit(0x9, 1, register_width=1)
    alert_2_enable = RWBit(0x9, 0, register_width=1)
    # Alert 3 Configuration - 0xa
    alert_3_int_clear = RWBit(0xa, 7, register_width=1)
    alert_3_temp_monitor = RWBit(0xa, 4, register_width=1)
    alert_3_temp_direction = RWBit(0xa, 3, register_width=1)
    alert_3_state = RWBit(0xa, 2, register_width=1)
    alert_3_mode = RWBit(0xa, 1, register_width=1)
    alert_3_enable = RWBit(0xa, 0, register_width=1)
    # Alert 4 Configuration - 0xb
    alert_4_int_clear = RWBit(0xb, 7, register_width=1)
    alert_4_temp_monitor = RWBit(0xb, 4, register_width=1)
    alert_4_temp_direction = RWBit(0xb, 3, register_width=1)
    alert_4_state = RWBit(0xb, 2, register_width=1)
    alert_4_mode = RWBit(0xb, 1, register_width=1)
    alert_4_enable = RWBit(0xb, 0, register_width=1)
    # Alert 1 Hysteresis - 0xc
    alert_hysteresis_1 = UnaryStruct(0xc, ">H")
    # Alert 2 Hysteresis - 0xd
    alert_hysteresis_2 = UnaryStruct(0xd, ">H")
    # Alert 3 Hysteresis - 0xe
    alert_hysteresis_3 = UnaryStruct(0xe, ">H")
    # Alert 4 Hysteresis - 0xf
    alert_hysteresis_4 = UnaryStruct(0xf, ">H")
    # Alert 1 Limit - 0x10
    alert_limit_1 = UnaryStruct(0x10, ">H")
    # Alert 2 Limit - 0x11
    alert_limit_2 = UnaryStruct(0x11, ">H")
    # Alert 3 Limit - 0x12
    alert_limit_3 = UnaryStruct(0x12, ">H")
    # Alert 4 Limit - 0x13
    alert_limit_4 = UnaryStruct(0x13, ">H")
    # Device ID/Revision - 0x20
    _device_id = ROBits(8, 0x20, 8, register_width=2, lsb_first=False)
    _revision_id = ROBits(8, 0x20, 0, register_width=2)

    # TODO: Consider using _device_id for address
    def __init__(self, i2c_bus, address=0x67):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)
        # TODO: update with device ID or revision ID?
        if self._device_id != 0x40:
            raise RuntimeError("Failed to find MCP9600 - check wiring!")

    @property
    def temperature(self):
        return self._hot_junction_temperature * 0.0625

    @property
    def cold_temperature(self):
        return self._cold_junction_temperature * 0.0625

    @property
    def temperature_delta(self):
        if self.temperature >= 0:
            return self._junctions_temperature_delta
        else:
            return self._junctions_temperature_delta - 4096

