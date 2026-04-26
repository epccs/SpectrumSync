# SpectrumSync SPSY-CREE-XNP

Insulated Metal Substrate (IMS) board with a Cree XP-N RGB+W and P-channel MOSFET (PMOS) bypass (or shunt) for a controller to operate with the pull down pads: GN1, PC1, RD1, and BL1.

## Details

A current driver is needed to deliver a constant current through the string of four LEDs (in the Cree XN-P device). On board, PMOS shunts are used to allow the current to bypass each LED with external control. The shunts don't block the current, so other LEDs in the string can still output light. When one of the shunts is enabled, current will begin to bypass the LED. When a shunt is enabled, the driver's capacitance will discharge, causing a current surge in the remaining LEDs. The SPSY-DRV01 mitigates the surge problem, but other LED drivers will probably need a power resistor (e.g., >5 Ohm, 20W) to reduce the surge to reasonable levels (LEDs do not handle current surges like ordinary diodes).

## Schematic

[Schematic](SPSY-CREE-XNP-sch.pdf)

## BOM (from KiCad iBOM plugin)

<https://htmlpreview.github.io/?https://github.com/epccs/SpectrumSync/blob/main/hardware/led-boards/SPSY-CREE-XNP/ibom.html>

## PCB-001A top side

![PCB-001A top side](PCB-001A_top.png)

## Notes

PCB-001A1 Rev of Gerbers is output from KiCad 10, previous was from KiCad 9.
