# SpectrumSync SPSY-CNTL01

LED RGB+W Control System with API interface.

## Details

First, a little rant: No one wants a phone app or remote to control their lights. More than a few of us are looking at things like OpenClaw and thinking this is the future of automation, though we also see the security issues. The truth is, I don't want the OpenClaw next door fiddling with my lights, nor do I want the one I use fiddling with their stuff. Regardless, for now, it is easy enough to have an AI write HTML and JS (or Python) that can operate the API while we let OpenClaw (and ilk) become safe.

## Schematic

[Schematic](SPSY-CNTL01-sch.pdf)

## BOM (from KiCad iBOM plugin)

<https://htmlpreview.github.io/?https://github.com/epccs/SpectrumSync/blob/main/hardware/controllers/SPSY-CNTL01/ibom.html>

## PCB-003A top side

![PCB-003A top side](PCB-003A_top.png)

## PCB-003A bottom side

![PCB-003A bottom side](PCB-003A_bottom.png)

## Power

The main power input can operate from 9 to 53V, which means a 48V battery won't have enough margin to support charging voltages, but well-regulated 48V supplies are good. Heavy equipment often has 24V alternators that clamp at about 65V (ISO 16750-2), and our little local clamp (TVS) shouldn't try to take over the alternators job (ours should act weakly, if at all, on it). A 1.5SMB56CA will let a 1 mA test current pass at 53V and allow gradually increasing current pulses up to 77V (about 20A), at which point it goes outside its limits. The rate of increase is an exponential, like the diode I-V equation, so it will not take over from the alternator's internal clamp but there is not much margine. Do not use this controller with power systems that lack load-dump clamps, whether 24V or 12V, as they will damage the controller's electronics.

## Internal Communication

There is a pair of microcontrolers, one is for managing power to the single board computer (SBC) as well as programing the other microcontroler for applications. The SBC is optianl, if present it could be a Raspery Pi Zero 2 running the Pi OS.

The Applicaiton microcontroler (MCU) has an I2C interface with the manager MCU as well as a UART interface to the multi-drop RS422 (full duplex). It is programed over the Microchip UPDI interface which can be selected by the Manager to operate over RS422 with a local or rmote SBC host. If the SBC is a remote board it will need to use the Manager on that board as well as the manager on the target to setup the RS422 as a point to point connection that goes into the UPDI port of the target Applicaiton microcontroler to be programmed. It is more or less the same if a local SBC host is to program the Application MCU on its local board, but only one manager is involved.

## History

A little about the back story for this setup. About six years ago I was tinkering with these AVR's that have a UPDI programing interface which is a UART based interface. Hopfuly it still works on R-Pi's as it did back then.

- <https://github.com/microchip-pic-avr-tools/pymcuprog>
